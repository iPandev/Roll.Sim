def EOM_A_r_dd(
    G, tw_v, I,
    A_r, A_r_d, A_l, A_l_dd, B_fr, B_fr_d, B_fl, B_rr, B_rr_d, B_rl,
    Ks_f_v, Ks_r_v, Karb_f_v, Karb_r_v, C_fr, C_rr
):
    return(
        (-tw_v**2)*(Ks_f_v*(A_r-B_fr) + C_fr*(A_r_d-B_fr_d) + Karb_f_v*((A_r-B_fr)-(A_l-B_fl)))/I +
        (-tw_v**2)*(Ks_r_v*(A_r-B_rr) + C_rr*(A_r_d-B_rr_d) + Karb_r_v*((A_r-B_rr)-(A_l-B_rl)))/I +
        G*tw_v/I +
        A_l_dd
    )