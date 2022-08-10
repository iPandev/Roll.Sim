import numpy as np
import math
from Func_virtual_track_conversion import RSF_virtual_track
from Func_update_damper_domain import RSF_update_damper_domain

def RSF_transient_response_VI(force_function, seconds, #Force function(Gs, w.r.t. time) and duration(s)
    tw_f, tw_r, Ks_f, Ks_r, Karb_f, Karb_r, Csb_f, Csr_f, Cfb_f, Cfr_f, Csb_r, Csr_r, Cfb_r, Cfr_r, #track widths(m), coil(N/m) and ARB(N/m, l-r relative displacement) spring rates, damper rates(N/(m/s))
    bypassV_fb, bypassV_fr, bypassV_rb, bypassV_rr, #damper bypass speeds (m/s)
    fls, frs, rls, rrs, flu, fru, rlu, rru, rotatingInertia, #masses (kg) and rotating inertia (kg*m**2)
    cg_height, rc_height_f, rc_height_r, tire_diam_f, tire_diam_r #suspension geometries (m)
    ):

    #Define timing array, dt for RK4 loop
    n=len(force_function)
    t = np.linspace(-0.1, seconds, num=n)
    dt = t[1]-t[0]

    #Initialize variable arrays, these will be the returned values.
    sprung_roll_angle = np.zeros(n)
    total_roll_angle = np.zeros(n)
    wheelDispF = np.zeros(n)
    wheelDispR = np.zeros(n)
    tireDispF = np.zeros(n)
    tireDispR = np.zeros(n)
    damperDispF = np.zeros(n)
    damperDispR = np.zeros(n)
    damperVelF = np.zeros(n)
    damperVelR = np.zeros(n)
    springDispF = np.zeros(n)
    springDispR = np.zeros(n)
    tireLoadFO = np.zeros(n)
    tireLoadFI = np.zeros(n)
    tireLoadRO = np.zeros(n)
    tireLoadRI = np.zeros(n)
    damperForceFO = np.zeros(n)
    damperForceFI = np.zeros(n)
    damperForceRO = np.zeros(n)
    damperForceRI = np.zeros(n)
    frontLLT = np.zeros(n)
    rearLLT = np.zeros(n)
    LLTr = np.zeros(n)
    
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
        print(i, f)

        #Function to assign correct damper value to C_xx based on Axx-Bxx
        iteration_damper_values = RSF_update_damper_domain(Csb_f_v, Csr_f_v, Cfb_f_v, Cfr_f_v, Csb_r_v, Csr_r_v, Cfb_r_v, Cfr_r_v, #damper rates (N/(m/s))
            bypassV_fb, bypassV_fr, bypassV_rb, bypassV_rr, #damper bypass speeds (m/s)
            A_r_d, A_l_d, B_fr_d, B_fl_d, B_rr_d, B_rl_d)
        C_fr = iteration_damper_values[0]
        C_fl = iteration_damper_values[1]
        C_rr = iteration_damper_values[2]
        C_rl = iteration_damper_values[3]

        #calculate elastic rolling moment (N*m)
        roll_moment = force_function[i]*9.80665*(frs+fls+rls+rrs)*(cg_height-rc_height_CG)
        roll_moment_next = force_function[i+1]*9.80665*(frs+fls+rls+rrs)*(cg_height-rc_height_CG)
        roll_moment_half_next = (roll_moment+roll_moment_next)/2

        #calculate geometric sprung weight transfer, f/r (N transfered to/ removed from SINGLE tire)
        wt_gsm_f = force_function[i]*9.80665*(fls+frs)*(rc_height_f/tw_f)
        wt_gsmNext_f = force_function[i+1]*9.80665*(fls+frs)*(rc_height_f/tw_f)
        wt_gsmHalfNext_f = (wt_gsm_f+wt_gsmNext_f)/2

        wt_gsm_r = force_function[i]*9.80665*(rls+rrs)*(rc_height_r/tw_r)
        wt_gsmNext_r = force_function[i+1]*9.80665*(rls+rrs)*(rc_height_r/tw_r)
        wt_gsmHalfNext_r = (wt_gsm_r+wt_gsmNext_r)/2

        #calculate geometric unsprung weight transfer, f/r (N transfered to/ removed from SINGLE tire)
        wt_gusm_f = force_function[i]*9.80665*(fru+flu)*(tire_diam_f/(2*tw_f))
        wt_gusmNext_f = force_function[i+1]*9.80665*(fru+flu)*(tire_diam_f/(2*tw_f))
        wt_gusmHalfNext_f = (wt_gusm_f+wt_gusmNext_f)/2

        wt_gusm_r = force_function[i]*9.80665*(rru+rlu)*(tire_diam_r/(2*tw_r))
        wt_gusmNext_r = force_function[i+1]*9.80665*(rru+rlu)*(tire_diam_r/(2*tw_r))
        wt_gusmHalfNext_r = (wt_gusm_r+wt_gusmNext_r)/2

        #calculate next step with RK4

        #assign/ compute output variables
        total_roll_angle[i] = math.atan((A_r-A_l)/tw_v)*180/math.pi #deg
    
    #Find peak/min values
    peakSRA = str(round(max(sprung_roll_angle), 3))
    peakTRA = str(round(max(total_roll_angle), 3))
    peakfV = str(round(max(damperVelF), 3))
    peakrV = str(round(max(damperVelR), 3))
    peakDampFO = str(round(abs(max(damperForceFO))))
    peakDampRO = str(round(abs(max(damperForceRO))))
    peakDampFI = str(round(abs(max(damperForceFI))))
    peakDampRI = str(round(abs(max(damperForceRI))))
    peakLoadFO = str(round(max(tireLoadFO)))
    peakLoadRO = str(round(max(tireLoadRO)))
    peakfLLT = str(round(100*max(frontLLT), 1))
    peakrLLT = str(round(100*max(rearLLT), 1))
    peakLLTR = str(round(max(LLTr), 3))
    minLLTR = str(round(min(LLTr), 3))

    return(t, sprung_roll_angle, damperVelF, damperVelR,
           damperForceFO, damperForceFI, damperForceRO, damperForceRI,
           tireLoadFO, tireLoadFI, tireLoadRO, tireLoadRI,
           100*frontLLT, 100*rearLLT, LLTr, #14
           
           #Returned None-types substitute depricated variables from v5 of this function, to maintain the positional value of other returns.
           peakSRA, None, peakfV, peakrV,
           peakDampFO, peakDampRO, peakDampFI, peakDampRI, #22
           peakLoadFO, peakLoadRO, #24
           peakfLLT, peakrLLT, peakLLTR, #27
           None, None, None, minLLTR, #31
          
           1000*(wheelDispF+tireDispF), 1000*(wheelDispR+tireDispR), #32, 33
           
           #new variables for v6 of this function
           total_roll_angle,

           peakTRA
           )