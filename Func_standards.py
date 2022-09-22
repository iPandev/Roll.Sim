"""
A document calculating vehicle performance using industry-accepted, or expert-published, formulas.
To be used as a reference to validate the Roll.Sim vehicle model.
"""

def RSF_standards(
    tw_f, tw_r, g_force, sprung_CM_height,
    sm_fr, sm_fl, sm_rr, sm_rl, usm_fr, usm_fl, usm_rr, usm_rl,
    tire_diam_f, tire_diam_r, aero_load_f, aero_load_r
):

    #Total lateral load transfer - Borrowed from Racecar Engineering articles by Claude Rouelle.
    sprung_weight_dist_f = (sm_fr + sm_fl) / (sm_fr + sm_fl + sm_rr + sm_rl)
    tw_v = tw_f + (tw_r - tw_f) * (1 - sprung_weight_dist_f)
    LT_elastic = g_force * 9.80665 * (sm_fr + sm_fl + sm_rr + sm_rl) * sprung_CM_height / tw_v
    LT_unsprung_f = g_force * 9.80665 * (usm_fr + usm_fl) * (tire_diam_f / 2) / (tw_f) #N
    LT_unsprung_r = g_force * 9.80665 * (usm_rr + usm_rl) * (tire_diam_r / 2) / (tw_r) #N Absolute value added to outside wheel.
    LT_total = LT_unsprung_f + LT_unsprung_r + LT_elastic
    LLT_percent = (LT_total + 9.80665 * (sm_fr + sm_rr + usm_fr + usm_rr) + aero_load_f/2 + aero_load_r/2) / (9.80665 * (sm_fl + sm_fr + sm_rl + sm_rr + usm_fl + usm_fr + usm_rl + usm_rr) + aero_load_f + aero_load_r)

    #Roll angle, and LLT_f, LLT_r, LLT_ratio as per Optimum G tech paper.

    return(
        LT_total, 100*LLT_percent
    )