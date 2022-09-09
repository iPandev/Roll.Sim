def RSF_update_damper_domain_2(Csb_v, Csr_v, Cfb_v, Cfr_v, #damper rates
    bypassV_bump, bypassV_reb, #damper bypass speeds
    A_d, B_d): #chassis and tire speeds

    #front-right damper
    c = Csr_v #assume slow rebound domain
    knee_force = 0
    damp_spd_offset = 0
    if A_d-B_d < -bypassV_reb: #if TRUE, damper is in fast rebound domain
        c = Cfr_v
        knee_force = -bypassV_reb * Csr_v
        damp_spd_offset = -bypassV_reb
    if A_d-B_d > 0: #if TRUE, damper is in some bump domain
        c = Csb_v #assume slow bump domain
        if A_d-B_d > bypassV_bump: #if TRUE, damper is in fast bump domain
            c = Cfb_v
            knee_force = bypassV_bump * Csb_v
            damp_spd_offset = bypassV_bump

    return(c, knee_force, damp_spd_offset) #damper rates to use for current iteration of RK4 Loop