import numpy as np
import math
from Func_virtual_track_conversion import RSF_virtual_track
from Func_update_damper_domain import RSF_update_damper_domain

def RSF_transient_response_VI(F, s, #Force function and duration
tw_f, tw_r, Ks_f, Ks_r, Karb_f, Karb_r, Csb_f, Csr_f, Cfb_f, Cfr_f, Csb_r, Csr_r, Cfb_r, Cfr_r): #track widths, coil and ARB spring rates, damper rates

    #Initialize variable arrays
    rollAngle = np.zeros(n)
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
    LLTR = np.zeros(n)

    #Define force function
    n=len(F)
    i=0
    t = np.linspace(-0.1, s, num=n)
    tNow = t[i]
    tNext = t[i+1]
    dt = tNext-tNow
    tHalfNext = tNow+dt/2

    #Define virtual track, wheel rates, and damper rates
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

    #Initialize ODE variables
    A_r = 0
    A_l = 0
    A_r_d = 0
    A_l_d = 0
    A_r_dd = 0
    A_l_dd = 0
    B_fr = 0
    B_fl = 0
    B_fr_d = 0
    B_fl_d = 0
    B_fr_dd = 0
    B_fl_dd = 0
    B_rr = 0
    B_rl = 0
    B_rr_d = 0
    B_rl_d = 0
    B_rr_dd = 0
    B_rl_dd = 0

    #Loop
        #Function to assign correct damper value to C_xx based on Axx-Bxx
        #Assign/ compute output variables

    return(t, rollAngle, damperVelF, damperVelR,
           damperForceFO, damperForceFI, damperForceRO, damperForceRI,
           tireLoadFO, tireLoadFI, tireLoadRO, tireLoadRI,
           100*frontLLT, 100*rearLLT, LLTR, #14
           
           peakRA, overshootRA, peakfV, peakrV,
           peakDampFO, peakDampRO, peakDampFI, peakDampRI, #22
           peakLoadFO, peakLoadRO, #24
           peakfLLT, peakrLLT, peakLLTR, #27
           overshootfLLT, overshootrLLT, overshootLLTR, minLLTR, #31
          
           1000*(wheelDispF+tireDispF), 1000*(wheelDispR+tireDispR)) #32, 33