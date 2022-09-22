import numpy as np
import math
from Func_virtual_track_conversion import RSF_virtual_track
from Func_update_damper_domain_2 import RSF_update_damper_domain_2
from Func_eqs_of_motion import EOM_A_r_dd, EOM_A_l_dd, EOM_B_fr_dd, EOM_B_fl_dd, EOM_B_rr_dd, EOM_B_rl_dd

def RSF_transient_response_6(force_function, seconds, #Force function(Gs, w.r.t. time) and duration(s)
    tw_f, tw_r, Ks_f, Ks_r, Karb_f, Karb_r, Csb_f, Csr_f, Cfb_f, Cfr_f, Csb_r, Csr_r, Cfb_r, Cfr_r, #track widths(m), coil(N/m) and ARB(N/m, l-r relative displacement) wheel rates, at-wheel damper rates(N/(m/s))
    bypassV_fb, bypassV_fr, bypassV_rb, bypassV_rr, #damper bypass speeds (m/s)
    fls, frs, rls, rrs, flu, fru, rlu, rru, roll_inertia, #masses (kg) and rotating inertia (kg*m**2)
    cg_height, rc_height_f, rc_height_r, tire_diam_f, tire_diam_r, #suspension geometries (m)
    WS_motion_ratio_f, WS_motion_ratio_r, WD_motion_ratio_f, WD_motion_ratio_r, #Wheel/spring or Wheel/damper motion ratios
    Kt_f, Kt_r, #tire spring rates (N/m)
    aero_load_f, aero_load_r #aerodynamic forces (N)
):

    #Define timing array, dt for RK4 loop
    n=len(force_function)-1
    t = np.linspace(-0.1, seconds, num=n)
    dt = t[1]-t[0]

    #Initialize variable arrays, these will be the returned values.
    chassis_disp_r = np.zeros(n)
    chassis_disp_l = np.zeros(n)
    sprung_roll_angle = np.zeros(n)
    total_roll_angle = np.zeros(n)
    damper_vel_fr = np.zeros(n)
    damper_vel_fl = np.zeros(n)
    damper_vel_rr = np.zeros(n)
    damper_vel_rl = np.zeros(n)
    damper_force_fr_v = np.zeros(n)
    damper_force_fl_v = np.zeros(n)
    damper_force_rr_v = np.zeros(n)
    damper_force_rl_v = np.zeros(n)
    tire_load_fr = np.zeros(n)
    tire_load_fl = np.zeros(n)
    tire_load_rr = np.zeros(n)
    tire_load_rl = np.zeros(n)
    LLT_f = np.zeros(n)
    LLT_r = np.zeros(n)
    LLT_ratio = np.zeros(n)
    WT_spring_roll_f = np.zeros(n)
    WT_spring_roll_r = np.zeros(n)
    WT_ARB_f = np.zeros(n)
    WT_ARB_r = np.zeros(n)
    WT_gsm_f = np.zeros(n)
    WT_gsm_r = np.zeros(n)
    WT_gusm_f = np.zeros(n)
    WT_gusm_r = np.zeros(n)
    WT_Ct_f = np.zeros(n)
    WT_Ct_r = np.zeros(n)
    DEBUG_tire_spring = np.zeros(n)
    DEBUG_tire_damp = np.zeros(n)
    DEBUG_tire_spring_rl = np.zeros(n)
    DEBUG_tire_damp_rl = np.zeros(n)
    
    #Other misc. variables
    rc_height_CG = rc_height_f+((fls+frs)/(frs+fls+rls+rrs))*(rc_height_r-rc_height_f)
    Ct_f = Kt_f/160 # targetting gamma = 0.2
    Ct_r = Kt_r/160 # targetting gamma = 0.2

    #Define virtual track, wheel rates, and damper rates.
    tw_v, Ks_f_v, Ks_r_v, Karb_f_v, Karb_r_v, Csb_f_v, Csr_f_v, Cfb_f_v, Cfr_f_v, Csb_r_v, Csr_r_v, Cfb_r_v, Cfr_r_v = RSF_virtual_track(
        tw_f, tw_r, Ks_f, Ks_r, Karb_f, Karb_r, Csb_f, Csr_f, Cfb_f, Cfr_f, Csb_r, Csr_r, Cfb_r, Cfr_r
    )

    #Initialize ODE variables. Roll.Sim always initializes the vehcile body at rest.
    A_r = 0 #m, chassis displacement right
    A_l = 0 #m, chassis displacement left
    A_r_d = 0 #m/s, chassis displacement right, 1st derivative
    A_l_d = 0 #m/s, chassis displacement left, 1st derivative
    A_r_dd = 0 #m/(s**2), chassis displacement right, 2nd derivative
    A_l_dd = 0 #m/(s**2), chassis displacement left, 2nd derivative
    B_fr = 0 #m, tire displacement front-right
    B_fl = 0 #m, tire displacement front-left
    B_fr_d = 0 #m/s, tire displacement front-right, 1st derivative
    B_fl_d = 0 #m/s, tire displacement front-left, 1st derivative
    B_rr = 0 #m, tire displacement rear-right
    B_rl = 0 #m, tire displacement rear-left
    B_rr_d = 0 #m/s, tire displacement rear-right, 1st derivative
    B_rl_d = 0 #m/s, tire displacement rear-left, 1st derivative

    #Begin Loop
    for i, f in enumerate(force_function[0:n]):

        #Function to assign correct damper value to C_xx based on Axx-Bxx
        C_fr, knee_force_fr, damp_spd_offset_fr = RSF_update_damper_domain_2(Csb_f_v, Csr_f_v, Cfb_f_v, Cfr_f_v, bypassV_fb, bypassV_fr, A_r_d, B_fr_d)
        C_fl, knee_force_fl, damp_spd_offset_fl = RSF_update_damper_domain_2(Csb_f_v, Csr_f_v, Cfb_f_v, Cfr_f_v, bypassV_fb, bypassV_fr, A_l_d, B_fl_d)
        C_rr, knee_force_rr, damp_spd_offset_rr = RSF_update_damper_domain_2(Csb_r_v, Csr_r_v, Cfb_r_v, Cfr_r_v, bypassV_rb, bypassV_rr, A_r_d, B_rr_d)
        C_rl, knee_force_rl, damp_spd_offset_rl = RSF_update_damper_domain_2(Csb_r_v, Csr_r_v, Cfb_r_v, Cfr_r_v, bypassV_rb, bypassV_rr, A_l_d, B_rl_d)

        #calculate elastic rolling moment (N*m)
        roll_moment = force_function[i]*9.80665*(frs+fls+rls+rrs)*(cg_height-rc_height_CG)
        roll_moment_Next = force_function[i+1]*9.80665*(frs+fls+rls+rrs)*(cg_height-rc_height_CG)
        roll_moment_HalfNext = (roll_moment+roll_moment_Next)/2

        #calculate geometric sprung weight transfer, f/r (N transfered to/ removed from SINGLE tire)
        wt_gsm_f = force_function[i]*9.80665*(fls+frs)*(rc_height_f/tw_f)
        wt_gsm_Next_f = force_function[i+1]*9.80665*(fls+frs)*(rc_height_f/tw_f)
        wt_gsm_HalfNext_f = (wt_gsm_f+wt_gsm_Next_f)/2
        WT_gsm_f[i] = wt_gsm_f*2

        wt_gsm_r = force_function[i]*9.80665*(rls+rrs)*(rc_height_r/tw_r)
        wt_gsm_Next_r = force_function[i+1]*9.80665*(rls+rrs)*(rc_height_r/tw_r)
        wt_gsm_HalfNext_r = (wt_gsm_r+wt_gsm_Next_r)/2
        WT_gsm_r[i] = wt_gsm_r*2

        #calculate geometric unsprung weight transfer, f/r (N transfered to/ removed from SINGLE tire)
        wt_gusm_f = force_function[i]*9.80665*(fru+flu)*(tire_diam_f/(2*tw_f))
        wt_gusm_Next_f = force_function[i+1]*9.80665*(fru+flu)*(tire_diam_f/(2*tw_f))
        wt_gusm_HalfNext_f = (wt_gusm_f+wt_gusm_Next_f)/2
        WT_gusm_f[i] = wt_gusm_f*2

        wt_gusm_r = force_function[i]*9.80665*(rru+rlu)*(tire_diam_r/(2*tw_r))
        wt_gusm_Next_r = force_function[i+1]*9.80665*(rru+rlu)*(tire_diam_r/(2*tw_r))
        wt_gusm_HalfNext_r = (wt_gusm_r+wt_gusm_Next_r)/2
        WT_gusm_r[i] = wt_gusm_r*2

        #assign/ compute output variables
        chassis_disp_r[i] = A_r
        chassis_disp_l[i] = A_l
        sprung_roll_angle[i] = math.atan((A_r-(B_fr+B_rr)/2-A_l+(B_fl+B_rl)/2)/tw_v)*180/math.pi #deg
        total_roll_angle[i] = math.atan((A_r-A_l)/tw_v)*180/math.pi #deg
        damper_vel_fr[i] = (A_r_d-B_fr_d) / (WD_motion_ratio_f) #m/s, at damper
        damper_vel_fl[i] = (A_l_d-B_fl_d) / (WD_motion_ratio_f) #m/s, at damper
        damper_vel_rr[i] = (A_r_d-B_rr_d) / (WD_motion_ratio_r) #m/s, at damper
        damper_vel_rl[i] = (A_l_d-B_rl_d) / (WD_motion_ratio_r) #m/s, at damper
        damper_force_fr_v[i] = C_fr * (A_r_d-B_fr_d-damp_spd_offset_fr) + knee_force_fr #N, at wheel, these vars are used as RK4 inputs and WT_damper, damper force (at damper) outputs.
        damper_force_fl_v[i] = C_fl * (A_l_d-B_fl_d-damp_spd_offset_fl) + knee_force_fl #N, at wheel
        damper_force_rr_v[i] = C_rr * (A_r_d-B_rr_d-damp_spd_offset_rr) + knee_force_rr #N, at wheel
        damper_force_rl_v[i] = C_rl * (A_l_d-B_rl_d-damp_spd_offset_rl) + knee_force_rl #N, at wheel
        tire_load_fr[i] = aero_load_f/2 + (frs+fru)*9.80665 + Kt_f*B_fr + Ct_f*B_fr_d #N
        tire_load_fl[i] = aero_load_f/2 + (fls+flu)*9.80665 + Kt_f*B_fl + Ct_f*B_fl_d #N
        tire_load_rr[i] = aero_load_r/2 + (rrs+rru)*9.80665 + Kt_r*B_rr + Ct_r*B_rr_d #N
        tire_load_rl[i] = aero_load_r/2 + (rls+rlu)*9.80665 + Kt_r*B_rl + Ct_r*B_rl_d #N
        LLT_f[i] = max(tire_load_fr[i] / (tire_load_fr[i]+tire_load_fl[i]), tire_load_fl[i] / (tire_load_fr[i]+tire_load_fl[i])) #%
        LLT_r[i] = max(tire_load_rr[i] / (tire_load_rr[i]+tire_load_rl[i]), tire_load_rl[i] / (tire_load_rr[i]+tire_load_rl[i])) #%
        LLT_ratio[i] = LLT_f[i] / LLT_r[i] #%
        WT_spring_roll_f[i] = Ks_f_v * (A_r-B_fr-(A_l-B_fl)) #N
        WT_spring_roll_r[i] = Ks_r_v * (A_r-B_rr-(A_l-B_rl)) #N
        WT_ARB_f[i] = Karb_f_v * ((A_r-B_fr) - (A_l-B_fl)) #N
        WT_ARB_r[i] = Karb_r_v * ((A_r-B_rr) - (A_l-B_rl)) #N
        WT_Ct_f[i] = Ct_f * (B_fr_d-B_fl_d) #N
        WT_Ct_r[i] = Ct_r * (B_rr_d-B_rl_d) #N
        DEBUG_tire_spring[i] = Kt_f*B_fl
        DEBUG_tire_damp[i] = Ct_f*B_fl_d
        DEBUG_tire_spring_rl[i] = Kt_r*B_rl
        DEBUG_tire_damp_rl[i] = Ct_r*B_rl_d

        #calculate next step with Runge-Kutta (4th order, 2nd derivative) for the following 6 DOF:
        #A_r_dd = F(force_function, A_r, A_r_d), interim vars c1-c4, d1-d4
        #A_l_dd = F(force_function, A_l, A_l_d), interim vars e1-e4, f1-f4
        #B_fr_dd = F(force_function, B_fr, B_fr_d), interim vars s1-s4, t1-t4
        #B_fl_dd = F(force_function, B_fl, B_fl_d), interim vars u1-u4, v1-v4
        #B_rr_dd = F(force_function, B_rr, B_rr_d), interim vars w1-w4, x1-x4
        #B_rl_dd = F(force_function, B_rl, B_rl_d), interim vars y1-y4, z1-z4

        A_r_dd = EOM_A_r_dd(roll_moment, tw_v, roll_inertia, A_r, A_r_d, A_l, A_l_dd, B_fr, B_fr_d, B_fl, B_rr, B_rr_d, B_rl, Ks_f_v, Ks_r_v, Karb_f_v, Karb_r_v, damper_force_fr_v[i], damper_force_rr_v[i])
        A_l_dd = EOM_A_l_dd(roll_moment, tw_v, roll_inertia, A_r, A_l_d, A_l, A_r_dd, B_fr, B_fl_d, B_fl, B_rr, B_rl_d, B_rl, Ks_f_v, Ks_r_v, Karb_f_v, Karb_r_v, damper_force_fl_v[i], damper_force_rl_v[i])

        c1 = dt * A_r_d
        d1 = dt * EOM_A_r_dd(roll_moment, tw_v, roll_inertia, A_r, A_r_d, A_l, A_l_dd, B_fr, B_fr_d, B_fl, B_rr, B_rr_d, B_rl, Ks_f_v, Ks_r_v, Karb_f_v, Karb_r_v, damper_force_fr_v[i], damper_force_rr_v[i])
        e1 = dt * A_l_d
        f1 = dt * EOM_A_l_dd(roll_moment, tw_v, roll_inertia, A_r, A_l_d, A_l, A_r_dd, B_fr, B_fl_d, B_fl, B_rr, B_rl_d, B_rl, Ks_f_v, Ks_r_v, Karb_f_v, Karb_r_v, damper_force_fl_v[i], damper_force_rl_v[i])
        s1 = dt * B_fr_d
        t1 = dt * EOM_B_fr_dd(wt_gsm_f, wt_gusm_f, A_r, A_r_d, A_l, B_fr, B_fr_d, B_fl, Ks_f_v, Karb_f_v, damper_force_fr_v[i], Kt_f, Ct_f, fru)
        u1 = dt * B_fl_d
        v1 = dt * EOM_B_fl_dd(wt_gsm_f, wt_gusm_f, A_r, A_l_d, A_l, B_fr, B_fl_d, B_fl, Ks_f_v, Karb_f_v, damper_force_fl_v[i], Kt_f, Ct_f, flu)
        w1 = dt * B_rr_d
        x1 = dt * EOM_B_rr_dd(wt_gsm_r, wt_gusm_r, A_r, A_r_d, A_l, B_rr, B_rr_d, B_rl, Ks_r_v, Karb_r_v, damper_force_rr_v[i], Kt_r, Ct_r, rru)
        y1 = dt * B_rl_d
        z1 = dt * EOM_B_rl_dd(wt_gsm_r, wt_gusm_r, A_r, A_l_d, A_l, B_rr, B_rl_d, B_rl, Ks_r_v, Karb_r_v, damper_force_rl_v[i], Kt_r, Ct_r, rlu)

        c2 = dt * (A_r_d + d1/2)
        d2 = dt * EOM_A_r_dd(roll_moment_HalfNext, tw_v, roll_inertia, (A_r+c1/2), (A_r_d+d1/2), A_l, A_l_dd, B_fr, B_fr_d, B_fl, B_rr, B_rr_d, B_rl, Ks_f_v, Ks_r_v, Karb_f_v, Karb_r_v, damper_force_fr_v[i], damper_force_rr_v[i])
        e2 = dt * (A_l_d + f1/2)
        f2 = dt * EOM_A_l_dd(roll_moment_HalfNext, tw_v, roll_inertia, A_r, (A_l_d+f1/2), (A_l+e1/2), A_r_dd, B_fr, B_fl_d, B_fl, B_rr, B_rl_d, B_rl, Ks_f_v, Ks_r_v, Karb_f_v, Karb_r_v, damper_force_fl_v[i], damper_force_rl_v[i])
        s2 = dt * (B_fr_d + t1/2)
        t2 = dt * EOM_B_fr_dd(wt_gsm_HalfNext_f, wt_gusm_HalfNext_f, A_r, A_r_d, A_l, (B_fr+s1/2), (B_fr_d+t1/2), B_fl, Ks_f_v, Karb_f_v, damper_force_fr_v[i], Kt_f, Ct_f, fru)
        u2 = dt * (B_fl_d + v1/2)
        v2 = dt * EOM_B_fl_dd(wt_gsm_HalfNext_f, wt_gusm_HalfNext_f, A_r, A_l_d, A_l, B_fr, (B_fl_d+v1/2), (B_fl+u1/2), Ks_f_v, Karb_f_v, damper_force_fl_v[i], Kt_f, Ct_f, flu)
        w2 = dt * (B_rr_d + x1/2)
        x2 = dt * EOM_B_rr_dd(wt_gsm_HalfNext_r, wt_gusm_HalfNext_r, A_r, A_r_d, A_l, (B_rr+w1/2), (B_rr_d+x1/2), B_rl, Ks_r_v, Karb_r_v, damper_force_rr_v[i], Kt_r, Ct_r, rru)
        y2 = dt * (B_rl_d + z1/2)
        z2 = dt * EOM_B_rl_dd(wt_gsm_HalfNext_r, wt_gusm_HalfNext_r, A_r, A_l_d, A_l, B_rr, (B_rl_d+z1/2), (B_rl+y1/2), Ks_r_v, Karb_r_v, damper_force_rl_v[i], Kt_r, Ct_r, rlu)

        c3 = dt * (A_r_d + d2/2)
        d3 = dt * EOM_A_r_dd(roll_moment_HalfNext, tw_v, roll_inertia, (A_r+c2/2), (A_r_d+d2/2), A_l, A_l_dd, B_fr, B_fr_d, B_fl, B_rr, B_rr_d, B_rl, Ks_f_v, Ks_r_v, Karb_f_v, Karb_r_v, damper_force_fr_v[i], damper_force_rr_v[i])
        e3 = dt * (A_l_d + f2/2)
        f3 = dt * EOM_A_l_dd(roll_moment_HalfNext, tw_v, roll_inertia, A_r, (A_l_d+f2/2), (A_l+e2/2), A_r_dd, B_fr, B_fl_d, B_fl, B_rr, B_rl_d, B_rl, Ks_f_v, Ks_r_v, Karb_f_v, Karb_r_v, damper_force_fl_v[i], damper_force_rl_v[i])
        s3 = dt * (B_fr_d + t2/2)
        t3 = dt * EOM_B_fr_dd(wt_gsm_HalfNext_f, wt_gusm_HalfNext_f, A_r, A_r_d, A_l, (B_fr+s2/2), (B_fr_d+t2/2), B_fl, Ks_f_v, Karb_f_v, damper_force_fr_v[i], Kt_f, Ct_f, fru)
        u3 = dt * (B_fl_d + v2/2)
        v3 = dt * EOM_B_fl_dd(wt_gsm_HalfNext_f, wt_gusm_HalfNext_f, A_r, A_l_d, A_l, B_fr, (B_fl_d+v2/2), (B_fl+u2/2), Ks_f_v, Karb_f_v, damper_force_fl_v[i], Kt_f, Ct_f, flu)
        w3 = dt * (B_rr_d + x2/2)
        x3 = dt * EOM_B_rr_dd(wt_gsm_HalfNext_r, wt_gusm_HalfNext_r, A_r, A_r_d, A_l, (B_rr+w2/2), (B_rr_d+x2/2), B_rl, Ks_r_v, Karb_r_v, damper_force_rr_v[i], Kt_r, Ct_r, rru)
        y3 = dt * (B_rl_d + z2/2)
        z3 = dt * EOM_B_rl_dd(wt_gsm_HalfNext_r, wt_gusm_HalfNext_r, A_r, A_l_d, A_l, B_rr, (B_rl_d+z2/2), (B_rl+y2/2), Ks_r_v, Karb_r_v, damper_force_rl_v[i], Kt_r, Ct_r, rlu)

        c4 = dt * (A_r_d + d3)
        d4 = dt * EOM_A_r_dd(roll_moment_Next, tw_v, roll_inertia, (A_r+c3), (A_r_d+d3), A_l, A_l_dd, B_fr, B_fr_d, B_fl, B_rr, B_rr_d, B_rl, Ks_f_v, Ks_r_v, Karb_f_v, Karb_r_v, damper_force_fr_v[i], damper_force_rr_v[i])
        e4 = dt * (A_l_d + f3)
        f4 = dt * EOM_A_l_dd(roll_moment_Next, tw_v, roll_inertia, A_r, (A_l_d+f3), (A_l+e3), A_r_dd, B_fr, B_fl_d, B_fl, B_rr, B_rl_d, B_rl, Ks_f_v, Ks_r_v, Karb_f_v, Karb_r_v, damper_force_fl_v[i], damper_force_rl_v[i])
        s4 = dt * (B_fr_d + t3)
        t4 = dt * EOM_B_fr_dd(wt_gsm_Next_f, wt_gusm_Next_f, A_r, A_r_d, A_l, (B_fr+s3), (B_fr_d+t3), B_fl, Ks_f_v, Karb_f_v, damper_force_fr_v[i], Kt_f, Ct_f, fru)
        u4 = dt * (B_fl_d + v3)
        v4 = dt * EOM_B_fl_dd(wt_gsm_Next_f, wt_gusm_Next_f, A_r, A_l_d, A_l, B_fr, (B_fl_d+v3), (B_fl+u3), Ks_f_v, Karb_f_v, damper_force_fl_v[i], Kt_f, Ct_f, flu)
        w4 = dt * (B_rr_d + x3)
        x4 = dt * EOM_B_rr_dd(wt_gsm_Next_r, wt_gusm_Next_r, A_r, A_r_d, A_l, (B_rr+w3), (B_rr_d+x3), B_rl, Ks_r_v, Karb_r_v, damper_force_rr_v[i], Kt_r, Ct_r, rru)
        y4 = dt * (B_rl_d + z3)
        z4 = dt * EOM_B_rl_dd(wt_gsm_Next_r, wt_gusm_Next_r, A_r, A_l_d, A_l, B_rr, (B_rl_d+z3), (B_rl+y3), Ks_r_v, Karb_r_v, damper_force_rl_v[i], Kt_r, Ct_r, rlu)

        #Assign next step's values for all variables
        A_r = A_r + (c1 + 2*c2 + 2*c3 + c4)/6
        A_r_d = A_r_d + (d1 + 2*d2 + 2*d3 + d4)/6
        A_l = A_l + (e1 + 2*e2 + 2*e3 + e4)/6
        A_l_d = A_l_d + (f1 + 2*f2 + 2*f3 + f4)/6
        B_fr = B_fr + (s1 + 2*s2 + 2*s3 + s4)/6
        B_fr_d = B_fr_d + (t1 + 2*t2 + 2*t3 + t4)/6
        B_fl = B_fl + (u1 + 2*u2 + 2*u3 + u4)/6
        B_fl_d = B_fl_d + (v1 + 2*v2 + 2*v3 + v4)/6
        B_rr = B_rr + (w1 + 2*w2 + 2*w3 + w4)/6
        B_rr_d = B_rr_d + (x1 + 2*x2 + 2*x3 + x4)/6
        B_rl = B_rl + (y1 + 2*y2 + 2*y3 + y4)/6
        B_rl_d = B_rl_d + (z1 + 2*z2 + 2*z3 + z4)/6

    #Calculate max/time tuples for overshoot calculations

    return(t, #s #0
        chassis_disp_r*1000, chassis_disp_l*1000, #mm #1,2
        sprung_roll_angle, total_roll_angle, #deg #3,4
        damper_vel_fr*1000, damper_vel_fl*1000, damper_vel_rr*1000, damper_vel_rl*1000, #mm/s #5,6,7,8
        damper_force_fr_v, damper_force_fl_v, damper_force_rr_v, damper_force_rl_v, #N #9,10,11,12
        tire_load_fr, tire_load_fl, tire_load_rr, tire_load_rl, #N #13,14,15,16
        LLT_f*100, LLT_r*100, LLT_ratio*100, #% #17,18,19

        WT_spring_roll_f, WT_spring_roll_r, #N #20,21
        WT_ARB_f, WT_ARB_r, #N #22,23
        WT_Ct_f, WT_Ct_r, #N #24,25
        WT_gsm_f, WT_gsm_r, WT_gusm_f, WT_gusm_r #N #26,27,28,29
    )