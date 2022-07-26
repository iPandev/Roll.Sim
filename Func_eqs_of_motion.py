"""
The heart of Roll.Sim, this document contains the equations of motion describing the Roll.Sim vehicle model.
"""

# Sprung Mass DOFs

def EOM_A_r_dd(
    G, tw_v, I,
    A_r, A_r_d, A_l, A_l_dd, B_fr, B_fr_d, B_fl, B_rr, B_rr_d, B_rl,
    Ks_f_v, Ks_r_v, Karb_f_v, Karb_r_v, damping_force_fr, damping_force_rr
):
    return(
        (-1)*(tw_v**2)*(Ks_f_v*(A_r-B_fr) + damping_force_fr + Karb_f_v*((A_r-B_fr)-(A_l-B_fl)))/I +
        (-1)*(tw_v**2)*(Ks_r_v*(A_r-B_rr) + damping_force_rr + Karb_r_v*((A_r-B_rr)-(A_l-B_rl)))/I +
        G*tw_v/I +
        A_l_dd
    )

def EOM_A_l_dd(
    G, tw_v, I,
    A_r, A_l_d, A_l, A_r_dd, B_fr, B_fl_d, B_fl, B_rr, B_rl_d, B_rl,
    Ks_f_v, Ks_r_v, Karb_f_v, Karb_r_v, damping_force_fl, damping_force_rl
):
    return(
        (-1)*(tw_v**2)*(Ks_f_v*(A_l-B_fl) + damping_force_fl + Karb_f_v*((A_l-B_fl)-(A_r-B_fr)))/I +
        (-1)*(tw_v**2)*(Ks_r_v*(A_l-B_rl) + damping_force_rl + Karb_r_v*((A_l-B_rl)-(A_r-B_rr)))/I -
        G*tw_v/I +
        A_r_dd
    )

# Unsprung Mass DOFs

def EOM_B_fr_dd(
    wt_gsm_f, wt_gusm_f,
    A_r, A_r_d, A_l, B_fr, B_fr_d, B_fl,
    Ks_f_v, Karb_f_v, damping_force_fr,
    Kt_f, Ct_f,
    fru
):
    return(
        (wt_gsm_f + wt_gusm_f +
        Ks_f_v*(A_r-B_fr) + damping_force_fr + Karb_f_v*((A_r-B_fr)-(A_l-B_fl)) -
        Kt_f*B_fr - Ct_f*B_fr_d) / 
        fru
    )

def EOM_B_fl_dd(
    wt_gsm_f, wt_gusm_f,
    A_r, A_l_d, A_l, B_fr, B_fl_d, B_fl,
    Ks_f_v, Karb_f_v, damping_force_fl,
    Kt_f, Ct_f,
    flu
):
    return(
        (-wt_gsm_f - wt_gusm_f +
        Ks_f_v*(A_l-B_fl) + damping_force_fl + Karb_f_v*((A_l-B_fl)-(A_r-B_fr)) -
        Kt_f*B_fl - Ct_f*B_fl_d) / 
        flu
    )

def EOM_B_rr_dd(
    wt_gsm_r, wt_gusm_r,
    A_r, A_r_d, A_l, B_rr, B_rr_d, B_rl,
    Ks_r_v, Karb_r_v, damping_force_rr,
    Kt_r, Ct_r,
    rru
):
    return(
        (wt_gsm_r + wt_gusm_r +
        Ks_r_v*(A_r-B_rr) + damping_force_rr + Karb_r_v*((A_r-B_rr)-(A_l-B_rl)) -
        Kt_r*B_rr - Ct_r*B_rr_d) / 
        rru
    )

def EOM_B_rl_dd(
    wt_gsm_r, wt_gusm_r,
    A_r, A_l_d, A_l, B_rr, B_rl_d, B_rl,
    Ks_r_v, Karb_r_v, damping_force_rl,
    Kt_r, Ct_r,
    rlu
):
    return(
        (-wt_gsm_r - wt_gusm_r +
        Ks_r_v*(A_l-B_rl) + damping_force_rl + Karb_r_v*((A_l-B_rl)-(A_r-B_rr)) -
        Kt_r*B_rl - Ct_r*B_rl_d) / 
        rlu
    )