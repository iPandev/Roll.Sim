#Incomplete and under construction. Roll.Sim_v0.2.0.py still uses this function's predecessor.

import numpy as np
import math
from Func_virtual_track_conversion import RSF_virtual_track
from Func_update_damper_domain import RSF_update_damper_domain
from Func_eqs_of_motion import EOM_A_r_dd, EOM_A_l_dd, EOM_B_fr_dd, EOM_B_fl_dd, EOM_B_rr_dd, EOM_B_rl_dd

def RSF_transient_response_6(force_function, seconds, #Force function(Gs, w.r.t. time) and duration(s)
    tw_f, tw_r, Ks_f, Ks_r, Karb_f, Karb_r, Csb_f, Csr_f, Cfb_f, Cfr_f, Csb_r, Csr_r, Cfb_r, Cfr_r, #track widths(m), coil(N/m) and ARB(N/m, l-r relative displacement) wheel rates, damper rates(N/(m/s))
    bypassV_fb, bypassV_fr, bypassV_rb, bypassV_rr, #damper bypass speeds (m/s)
    fls, frs, rls, rrs, flu, fru, rlu, rru, roll_inertia, #masses (kg) and rotating inertia (kg*m**2)
    cg_height, rc_height_f, rc_height_r, tire_diam_f, tire_diam_r, #suspension geometries (m)
    WS_motion_ratio_f, WS_motion_ratio_r, WD_motion_ratio_f, WD_motion_ratio_r, #Wheel/spring or Wheel/damper motion ratios
    Kt_f, Kt_r, Ct_f, Ct_r, #tire spring (N/m) and damping (N/(m/s)) rates
    aero_load_f, aero_load_r #aerodynamic forces (N)
):

    #Define timing array, dt for RK4 loop
    n=len(force_function)
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
    damper_force_fr = np.zeros(n)
    damper_force_fl = np.zeros(n)
    damper_force_rr = np.zeros(n)
    damper_force_rl = np.zeros(n)
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
    #WT_damper_f = computed from damper_force_fr and damper_force_fl arrays in main file to save mem in this function
    #WT_damper_R = computed from damper_force_rr and damper_force_rl arrays in main file to save mem in this function
    WT_gsm_f = np.zeros(n) #opportunity to remove wt_gsm_f variable by referencing this array
    WT_gsm_r = np.zeros(n) #opportunity to remove wt_gsm_r variable by referencing this array
    WT_gusm_f = np.zeros(n) #opportunity to remove wt_gusm_f variable by referencing this array
    WT_gusm_r = np.zeros(n) #opportunity to remove wt_gusm_r variable by referencing this array
    WT_Ct_f = np.zeros(n)
    WT_Ct_r = np.zeros(n)
    
    #Other misc. variables
    rc_height_CG = rc_height_f+((fls+frs)/(frs+fls+rls+rrs))*(rc_height_r-rc_height_f)

    #Define virtual track, wheel rates, and damper rates.
    virtual_vars = RSF_virtual_track(tw_f, tw_r, Ks_f, Ks_r, Karb_f, Karb_r, Csb_f, Csr_f, Cfb_f, Cfr_f, Csb_r, Csr_r, Cfb_r, Cfr_r)

    tw_v = virtual_vars[0]
    Ks_f_v = virtual_vars[1]
    Ks_r_v = virtual_vars[2]
    Karb_f_v = virtual_vars[3]
    Karb_r_v = virtual_vars[4]
    Csb_f_v = virtual_vars[5]
    Csr_f_v = virtual_vars[6]
    Cfb_f_v = virtual_vars[7]
    Cfr_f_v = virtual_vars[8]
    Csb_r_v = virtual_vars[9]
    Csr_r_v = virtual_vars[10]
    Cfb_r_v = virtual_vars[11]
    Cfr_r_v = virtual_vars[12]

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
    B_fr_dd = 0 #m/(s**2), tire displacement front-right, 2nd derivative
    B_fl_dd = 0 #m/(s**2), tire displacement front-left, 2nd derivative
    B_rr = 0 #m, tire displacement rear-right
    B_rl = 0 #m, tire displacement rear-left
    B_rr_d = 0 #m/s, tire displacement rear-right, 1st derivative
    B_rl_d = 0 #m/s, tire displacement rear-left, 1st derivative
    B_rr_dd = 0 #m/(s**2), tire displacement rear-right, 2nd derivative
    B_rl_dd = 0 #m/(s**2), tire displacement rear-left, 2nd derivative

    #Begin Loop
    for i, f in enumerate(force_function):
        
        #Don't want to run this check every iteration. Consider a stop-gap for now.
        if i == len(force_function)-1:
            break

        #Function to assign correct damper value to C_xx based on Axx-Bxx
        iteration_damper_values = RSF_update_damper_domain(Csb_f_v, Csr_f_v, Cfb_f_v, Cfr_f_v, Csb_r_v, Csr_r_v, Cfb_r_v, Cfr_r_v, #damper rates (N/(m/s))
            bypassV_fb, bypassV_fr, bypassV_rb, bypassV_rr, #damper bypass speeds (m/s)
            A_r_d, A_l_d, B_fr_d, B_fl_d, B_rr_d, B_rl_d)
        C_fr = iteration_damper_values[0] #N/(m/s)
        C_fl = iteration_damper_values[1] #N/(m/s)
        C_rr = iteration_damper_values[2] #N/(m/s)
        C_rl = iteration_damper_values[3] #N/(m/s)

        #calculate elastic rolling moment (N*m)
        roll_moment = force_function[i]*9.80665*(frs+fls+rls+rrs)*(cg_height-rc_height_CG)
        roll_moment_Next = force_function[i+1]*9.80665*(frs+fls+rls+rrs)*(cg_height-rc_height_CG)
        roll_moment_HalfNext = (roll_moment+roll_moment_Next)/2

        #calculate geometric sprung weight transfer, f/r (N transfered to/ removed from SINGLE tire)
        wt_gsm_f = force_function[i]*9.80665*(fls+frs)*(rc_height_f/tw_f)
        wt_gsm_Next_f = force_function[i+1]*9.80665*(fls+frs)*(rc_height_f/tw_f)
        wt_gsm_HalfNext_f = (wt_gsm_f+wt_gsm_Next_f)/2
        WT_gsm_f[i] = wt_gsm_f

        wt_gsm_r = force_function[i]*9.80665*(rls+rrs)*(rc_height_r/tw_r)
        wt_gsm_Next_r = force_function[i+1]*9.80665*(rls+rrs)*(rc_height_r/tw_r)
        wt_gsm_HalfNext_r = (wt_gsm_r+wt_gsm_Next_r)/2
        WT_gsm_r[i] = wt_gsm_r

        #calculate geometric unsprung weight transfer, f/r (N transfered to/ removed from SINGLE tire)
        wt_gusm_f = force_function[i]*9.80665*(fru+flu)*(tire_diam_f/(2*tw_f))
        wt_gusm_Next_f = force_function[i+1]*9.80665*(fru+flu)*(tire_diam_f/(2*tw_f))
        wt_gusm_HalfNext_f = (wt_gusm_f+wt_gusm_Next_f)/2
        WT_gusm_f[i] = wt_gusm_f

        wt_gusm_r = force_function[i]*9.80665*(rru+rlu)*(tire_diam_r/(2*tw_r))
        wt_gusm_Next_r = force_function[i+1]*9.80665*(rru+rlu)*(tire_diam_r/(2*tw_r))
        wt_gusm_HalfNext_r = (wt_gusm_r+wt_gusm_Next_r)/2
        WT_gusm_r[i] = wt_gusm_r

        #assign/ compute output variables
        chassis_disp_r[i] = A_r
        chassis_disp_l[i] = A_l
        sprung_roll_angle[i] = math.atan((A_r-(B_fr+B_rr)/2-A_l+(B_fl+B_rl)/2)/tw_v)*180/math.pi #deg
        total_roll_angle[i] = math.atan((A_r-A_l)/tw_v)*180/math.pi #deg
        damper_vel_fr[i] = (A_r_d-B_fr_d) / (WD_motion_ratio_f) #m/s
        damper_vel_fl[i] = (A_l_d-B_fl_d) / (WD_motion_ratio_f) #m/s
        damper_vel_rr[i] = (A_r_d-B_rr_d) / (WD_motion_ratio_r) #m/s
        damper_vel_rl[i] = (A_l_d-B_rl_d) / (WD_motion_ratio_r) #m/s
        damper_force_fr[i] = C_fr * (A_r_d-B_fr_d) / (WD_motion_ratio_f) #N
        damper_force_fl[i] = C_fl * (A_l_d-B_fl_d) / (WD_motion_ratio_f) #N
        damper_force_rr[i] = C_rr * (A_r_d-B_rr_d) / (WD_motion_ratio_r) #N
        damper_force_rl[i] = C_rl * (A_l_d-B_rl_d) / (WD_motion_ratio_r) #N
        tire_load_fr[i] = aero_load_f + (frs+fru)*9.80665 + Kt_f*B_fr + Ct_f*B_fr_d #N TODO: unsprung inertial force?
        tire_load_fl[i] = aero_load_f + (fls+flu)*9.80665 + Kt_f*B_fl + Ct_f*B_fl_d #N TODO: unsprung inertial force?
        tire_load_rr[i] = aero_load_r + (rrs+rru)*9.80665 + Kt_r*B_rr + Ct_r*B_rr_d #N TODO: unsprung inertial force?
        tire_load_rl[i] = aero_load_r + (rls+rlu)*9.80665 + Kt_r*B_rl + Ct_r*B_rl_d #N TODO: unsprung inertial force?
        LLT_f[i] = tire_load_fr[i] / (tire_load_fr[i]+tire_load_fl[i])
        LLT_r[i] = tire_load_rr[i] / (tire_load_rr[i]+tire_load_rl[i])
        LLT_ratio[i] = LLT_f[i] / LLT_r[i]
        WT_spring_roll_f[i] = Ks_f_v * (A_r-B_fr-(A_l-B_fl)) / (WS_motion_ratio_f) #N
        WT_spring_roll_r[i] = Ks_r_v * (A_r-B_rr-(A_l-B_rl)) / (WS_motion_ratio_r) #N
        WT_ARB_f[i] = Karb_f_v * (A_r-B_fr) - (A_l-B_fl) #N
        WT_ARB_r[i] = Karb_r_v * (A_r-B_rr) - (A_l-B_rl) #N
        WT_Ct_f[i] = Ct_f * (B_fr_d-B_fl_d) #N
        WT_Ct_r[i] = Ct_r * (B_rr_d-B_rl_d) #N

        #calculate next step with Runge-Kutta (4th order, 2nd derivative) for the following 6 DOF:
        #A_r_dd = F(force_function, A_r, A_r_d), interim vars c1-c4, d1-d4
        #A_l_dd = F(force_function, A_l, A_l_d), interim vars e1-e4, f1-f4
        #B_fr_dd = F(force_function, B_fr, B_fr_d), interim vars s1-s4, t1-t4
        #B_fl_dd = F(force_function, B_fl, B_fl_d), interim vars u1-u4, v1-v4
        #B_rr_dd = F(force_function, B_rr, B_rr_d), interim vars w1-w4, x1-x4
        #B_rl_dd = F(force_function, B_rl, B_rl_d), interim vars y1-y4, z1-z4

        A_r_dd = EOM_A_r_dd(roll_moment, tw_v, roll_inertia, A_r, A_r_d, A_l, A_l_dd, B_fr, B_fr_d, B_fl, B_rr, B_rr_d, B_rl, Ks_f_v, Ks_r_v, Karb_f_v, Karb_r_v, C_fr, C_rr)
        A_l_dd = EOM_A_l_dd(roll_moment, tw_v, roll_inertia, A_r, A_l_d, A_l, A_r_dd, B_fr, B_fl_d, B_fl, B_rr, B_rl_d, B_rl, Ks_f_v, Ks_r_v, Karb_f_v, Karb_r_v, C_fr, C_rr)
        B_fr_dd = EOM_B_fr_dd(wt_gsm_f, wt_gusm_f, A_r, A_r_d, A_l, B_fr, B_fr_d, B_fl, Ks_f_v, Karb_f_v, C_fr, Kt_f, Ct_f, fru)
        B_fl_dd = EOM_B_fl_dd(wt_gsm_f, wt_gusm_f, A_r, A_l_d, A_l, B_fr, B_fl_d, B_fl, Ks_f_v, Karb_f_v, C_fl, Kt_f, Ct_f, flu)
        B_rr_dd = EOM_B_rr_dd(wt_gsm_r, wt_gusm_r, A_r, A_r_d, A_l, B_rr, B_rr_d, B_rl, Ks_r_v, Karb_r_v, C_rr, Kt_r, Ct_r, rru)
        B_rl_dd = EOM_B_rl_dd(wt_gsm_r, wt_gusm_r, A_r, A_l_d, A_l, B_rr, B_rl_d, B_rl, Ks_r_v, Karb_r_v, C_rl, Kt_r, Ct_r, rlu)

        c1 = dt * A_r_d
        d1 = dt * EOM_A_r_dd(roll_moment, tw_v, roll_inertia, A_r, A_r_d, A_l, A_l_dd, B_fr, B_fr_d, B_fl, B_rr, B_rr_d, B_rl, Ks_f_v, Ks_r_v, Karb_f_v, Karb_r_v, C_fr, C_rr)
        e1 = dt * A_l_d
        f1 = dt * EOM_A_l_dd(roll_moment, tw_v, roll_inertia, A_r, A_l_d, A_l, A_r_dd, B_fr, B_fl_d, B_fl, B_rr, B_rl_d, B_rl, Ks_f_v, Ks_r_v, Karb_f_v, Karb_r_v, C_fr, C_rr)
        s1 = dt * B_fr_d
        t1 = dt * EOM_B_fr_dd(wt_gsm_f, wt_gusm_f, A_r, A_r_d, A_l, B_fr, B_fr_d, B_fl, Ks_f_v, Karb_f_v, C_fr, Kt_f, Ct_f, fru)
        u1 = dt * B_fl_d
        v1 = dt * EOM_B_fl_dd(wt_gsm_f, wt_gusm_f, A_r, A_l_d, A_l, B_fr, B_fl_d, B_fl, Ks_f_v, Karb_f_v, C_fl, Kt_f, Ct_f, flu)
        w1 = dt * B_rr_d
        x1 = dt * EOM_B_rr_dd(wt_gsm_r, wt_gusm_r, A_r, A_r_d, A_l, B_rr, B_rr_d, B_rl, Ks_r_v, Karb_r_v, C_rr, Kt_r, Ct_r, rru)
        y1 = dt * B_rl_d
        z1 = dt * EOM_B_rl_dd(wt_gsm_r, wt_gusm_r, A_r, A_l_d, A_l, B_rr, B_rl_d, B_rl, Ks_r_v, Karb_r_v, C_rl, Kt_r, Ct_r, rlu)

        c2 = dt * (A_r_d + d1/2)
        d2 = dt * EOM_A_r_dd(roll_moment_HalfNext, tw_v, roll_inertia, (A_r+c1/2), (A_r_d+d1/2), A_l, A_l_dd, B_fr, B_fr_d, B_fl, B_rr, B_rr_d, B_rl, Ks_f_v, Ks_r_v, Karb_f_v, Karb_r_v, C_fr, C_rr)
        e2 = dt * (A_l_d + f1/2)
        f2 = dt * EOM_A_l_dd(roll_moment_HalfNext, tw_v, roll_inertia, A_r, (A_l_d+f1/2), (A_l+e1/2), A_r_dd, B_fr, B_fl_d, B_fl, B_rr, B_rl_d, B_rl, Ks_f_v, Ks_r_v, Karb_f_v, Karb_r_v, C_fr, C_rr)
        s2 = dt * (B_fr_d + t1/2)
        t2 = dt * EOM_B_fr_dd(wt_gsm_HalfNext_f, wt_gusm_HalfNext_f, A_r, A_r_d, A_l, (B_fr+s1/2), (B_fr_d+t1/2), B_fl, Ks_f_v, Karb_f_v, C_fr, Kt_f, Ct_f, fru)
        u2 = dt * (B_fl_d + v1/2)
        v2 = dt * EOM_B_fl_dd(wt_gsm_HalfNext_f, wt_gusm_HalfNext_f, A_r, A_l_d, A_l, B_fr, (B_fl_d+v1/2), (B_fl+u1/2), Ks_f_v, Karb_f_v, C_fl, Kt_f, Ct_f, flu)
        w2 = dt * (B_rr_d + x1/2)
        x2 = dt * EOM_B_rr_dd(wt_gsm_HalfNext_r, wt_gusm_HalfNext_r, A_r, A_r_d, A_l, (B_rr+w1/2), (B_rr_d+x1/2), B_rl, Ks_r_v, Karb_r_v, C_rr, Kt_r, Ct_r, rru)
        y2 = dt * (B_rl_d + z1/2)
        z2 = dt * EOM_B_rl_dd(wt_gsm_HalfNext_r, wt_gusm_HalfNext_r, A_r, A_l_d, A_l, B_rr, (B_rl_d+z1/2), (B_rl+y1/2), Ks_r_v, Karb_r_v, C_rl, Kt_r, Ct_r, rlu)

        c3 = dt * (A_r_d + d2/2)
        d3 = dt * EOM_A_r_dd(roll_moment_HalfNext, tw_v, roll_inertia, (A_r+c2/2), (A_r_d+d2/2), A_l, A_l_dd, B_fr, B_fr_d, B_fl, B_rr, B_rr_d, B_rl, Ks_f_v, Ks_r_v, Karb_f_v, Karb_r_v, C_fr, C_rr)
        e3 = dt * (A_l_d + f2/2)
        f3 = dt * EOM_A_l_dd(roll_moment_HalfNext, tw_v, roll_inertia, A_r, (A_l_d+f2/2), (A_l+e2/2), A_r_dd, B_fr, B_fl_d, B_fl, B_rr, B_rl_d, B_rl, Ks_f_v, Ks_r_v, Karb_f_v, Karb_r_v, C_fr, C_rr)
        s3 = dt * (B_fr_d + t2/2)
        t3 = dt * EOM_B_fr_dd(wt_gsm_HalfNext_f, wt_gusm_HalfNext_f, A_r, A_r_d, A_l, (B_fr+s2/2), (B_fr_d+t2/2), B_fl, Ks_f_v, Karb_f_v, C_fr, Kt_f, Ct_f, fru)
        u3 = dt * (B_fl_d + v2/2)
        v3 = dt * EOM_B_fl_dd(wt_gsm_HalfNext_f, wt_gusm_HalfNext_f, A_r, A_l_d, A_l, B_fr, (B_fl_d+v2/2), (B_fl+u2/2), Ks_f_v, Karb_f_v, C_fl, Kt_f, Ct_f, flu)
        w3 = dt * (B_rr_d + x2/2)
        x3 = dt * EOM_B_rr_dd(wt_gsm_HalfNext_r, wt_gusm_HalfNext_r, A_r, A_r_d, A_l, (B_rr+w2/2), (B_rr_d+x2/2), B_rl, Ks_r_v, Karb_r_v, C_rr, Kt_r, Ct_r, rru)
        y3 = dt * (B_rl_d + z2/2)
        z3 = dt * EOM_B_rl_dd(wt_gsm_HalfNext_r, wt_gusm_HalfNext_r, A_r, A_l_d, A_l, B_rr, (B_rl_d+z2/2), (B_rl+y2/2), Ks_r_v, Karb_r_v, C_rl, Kt_r, Ct_r, rlu)

        c4 = dt * (A_r_d + d3)
        d4 = dt * EOM_A_r_dd(roll_moment_Next, tw_v, roll_inertia, (A_r+c3), (A_r_d+d3), A_l, A_l_dd, B_fr, B_fr_d, B_fl, B_rr, B_rr_d, B_rl, Ks_f_v, Ks_r_v, Karb_f_v, Karb_r_v, C_fr, C_rr)
        e4 = dt * (A_l_d + f3)
        f4 = dt * EOM_A_l_dd(roll_moment_Next, tw_v, roll_inertia, A_r, (A_l_d+f3), (A_l+e3), A_r_dd, B_fr, B_fl_d, B_fl, B_rr, B_rl_d, B_rl, Ks_f_v, Ks_r_v, Karb_f_v, Karb_r_v, C_fr, C_rr)
        s4 = dt * (B_fr_d + t3)
        t4 = dt * EOM_B_fr_dd(wt_gsm_Next_f, wt_gusm_Next_f, A_r, A_r_d, A_l, (B_fr+s3), (B_fr_d+t3), B_fl, Ks_f_v, Karb_f_v, C_fr, Kt_f, Ct_f, fru)
        u4 = dt * (B_fl_d + v3)
        v4 = dt * EOM_B_fl_dd(wt_gsm_Next_f, wt_gusm_Next_f, A_r, A_l_d, A_l, B_fr, (B_fl_d+v3), (B_fl+u3), Ks_f_v, Karb_f_v, C_fl, Kt_f, Ct_f, flu)
        w4 = dt * (B_rr_d + x3)
        x4 = dt * EOM_B_rr_dd(wt_gsm_Next_r, wt_gusm_Next_r, A_r, A_r_d, A_l, (B_rr+w3), (B_rr_d+x3), B_rl, Ks_r_v, Karb_r_v, C_rr, Kt_r, Ct_r, rru)
        y4 = dt * (B_rl_d + z3)
        z4 = dt * EOM_B_rl_dd(wt_gsm_Next_r, wt_gusm_Next_r, A_r, A_l_d, A_l, B_rr, (B_rl_d+z3), (B_rl+y3), Ks_r_v, Karb_r_v, C_rl, Kt_r, Ct_r, rlu)

        A_r_Next = A_r + (c1 + 2*c2 + 2*c3 + c4)/6
        A_r_d_Next = A_r_d + (d1 + 2*d2 + 2*d3 + d4)/6
        A_l_Next = A_l + (e1 + 2*e2 + 2*e3 + e4)/6
        A_l_d_Next = A_l_d + (f1 + 2*f2 + 2*f3 + f4)/6
        B_fr_Next = B_fr + (s1 + 2*s2 + 2*s3 + s4)/6
        B_fr_d_Next = B_fr_d + (t1 + 2*t2 + 2*t3 + t4)/6
        B_fl_Next = B_fl + (u1 + 2*u2 + 2*u3 + u4)/6
        B_fl_d_Next = B_fl_d + (v1 + 2*v2 + 2*v3 + v4)/6
        B_rr_Next = B_rr + (w1 + 2*w2 + 2*w3 + w4)/6
        B_rr_d_Next = B_rr_d + (x1 + 2*x2 + 2*x3 + x4)/6
        B_rl_Next = B_rl + (y1 + 2*y2 + 2*y3 + y4)/6
        B_rl_d_Next = B_rl_d + (z1 + 2*z2 + 2*z3 + z4)/6

        #Reset variables for next iteration
        A_r = A_r_Next
        A_r_d = A_r_d_Next
        A_l = A_l_Next
        A_l_d = A_l_d_Next
        B_fr = B_fr_Next
        B_fr_d = B_fr_d_Next
        B_fl = B_fl_Next
        B_fl_d = B_fl_d_Next
        B_rr = B_rr_Next
        B_rr_d = B_rr_d_Next
        B_rl = B_rl_Next
        B_rl_d = B_rl_d_Next

    #Find peak/min values
    peakSRA = str(round(max(sprung_roll_angle), 3))
    peakTRA = str(round(max(total_roll_angle), 3))
    #peakDampFO = str(round(abs(max(damperForceFO))))
    #peakDampRO = str(round(abs(max(damperForceRO))))
    #peakDampFI = str(round(abs(max(damperForceFI))))
    #peakDampRI = str(round(abs(max(damperForceRI))))
    #peakLoadFO = str(round(max(tireLoadFO)))
    #peakLoadRO = str(round(max(tireLoadRO)))
    #peakfLLT = str(round(100*max(frontLLT), 1))
    #peakrLLT = str(round(100*max(rearLLT), 1))
    #peakLLTR = str(round(max(LLTr), 3))
    #minLLTR = str(round(min(LLTr), 3))

    return(t, #time array (s)
        total_roll_angle, #deg
        damper_vel_fr, damper_vel_fl, damper_vel_rr, damper_vel_rl, #m/s
        damper_force_fr, damper_force_fl, damper_force_rr, damper_force_rl, #N
        tire_load_fr, tire_load_fl, tire_load_rr, tire_load_rl, #N
        chassis_disp_r, chassis_disp_l #N
    )