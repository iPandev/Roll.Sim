#good candidate for a test script because so much visually confusing nomenclature

def RSF_update_damper_domain(Csb_f_v, Csr_f_v, Cfb_f_v, Cfr_f_v, Csb_r_v, Csr_r_v, Cfb_r_v, Cfr_r_v, #damper rates
    bypassV_fb, bypassV_fr, bypassV_rb, bypassV_rr, #damper bypass speeds
    A_r_d, A_l_d, B_fr_d, B_fl_d, B_rr_d, B_rl_d): #chassis and tire speeds

    #front-right damper
    if A_r_d-B_fr_d > 0: #if TRUE, damper is in some bump domain
        C_fr = Csb_f_v #assume slow bump domain
        if A_r_d-B_fr_d > bypassV_fb: #if TRUE, damper is in fast bump domain
            C_fr = Cfb_f_v
    else: #if ELSE, damper is in some rebound domain
        C_fr = Csr_f_v #assume slow rebound domain
        if A_r_d-B_fr_d > bypassV_fr: #if TRUE, damper is in fast rebound domain
            C_fr = Cfr_f_v
    
    #front-left damper
    if A_l_d-B_fl_d > 0: #if TRUE, damper is in some bump domain
        C_fl = Csb_f_v #assume slow bump domain
        if A_l_d-B_fl_d > bypassV_fb: #if TRUE, damper is in fast bump domain
            C_fl = Cfb_f_v
    else: #if ELSE, damper is in some rebound domain
        C_fl = Csr_f_v #assume slow rebound domain
        if A_l_d-B_fl_d > bypassV_fr: #if TRUE, damper is in fast rebound domain
            C_fl = Cfr_f_v

    #rear-right damper
    if A_r_d-B_rr_d > 0: #if TRUE, damper is in some bump domain
        C_rr = Csb_r_v #assume slow bump domain
        if A_r_d-B_rr_d > bypassV_rb: #if TRUE, damper is in fast bump domain
            C_rr = Cfb_r_v
    else: #if ELSE, damper is in some rebound domain
        C_rr = Csr_r_v #assume slow rebound domain
        if A_r_d-B_rr_d > bypassV_rr: #if TRUE, damper is in fast rebound domain
            C_rr = Cfr_r_v
    
    #rear-left damper
    if A_l_d-B_rl_d > 0: #if TRUE, damper is in some bump domain
        C_rl = Csb_r_v #assume slow bump domain
        if A_l_d-B_rl_d > bypassV_rb: #if TRUE, damper is in fast bump domain
            C_rl = Cfb_r_v
    else: #if ELSE, damper is in some rebound domain
        C_rl = Csr_r_v #assume slow rebound domain
        if A_l_d-B_rl_d > bypassV_rr: #if TRUE, damper is in fast rebound domain
            C_rl = Cfr_r_v

    return(C_fr, C_fl, C_rr, C_rl) #damper rates to use for current iteration of RK4 Loop