# A function to convert the spring rate and all 4 damper rates of all 4 wheels, to the at-wheel spring rates and at-wheel damper rates calcualted at a virtual track width, which is the average of the front and rear track widths.

def virtual_track_conversion(tw_f, tw_r,
    f_wheel_rate,
    r_wheel_rate,
    f_slow_bump_rate,
    f_slow_rebound_rate,
    f_fast_bump_rate,
    f_fast_rebound_rate,
    r_slow_bump_rate,
    r_slow_rebound_rate,
    r_fast_bump_rate,
    r_fast_rebound_rate):

    tw_v = (tw_f + tw_r)/2
    f_wheel_rate_virtual = f_wheel_rate*((tw_f/tw_v)**2)
    r_wheel_rate_virtual = r_wheel_rate*((tw_r/tw_v)**2)
    f_slow_bump_rate_virtual = f_slow_bump_rate*((tw_f/tw_v)**2)
    f_slow_rebound_rate_virtual = f_slow_rebound_rate*((tw_f/tw_v)**2)
    f_fast_bump_rate_virtual = f_fast_bump_rate*((tw_f/tw_v)**2)
    f_fast_rebound_rate_virtual = f_fast_rebound_rate*((tw_f/tw_v)**2)
    r_slow_bump_rate_virtual = r_slow_bump_rate*((tw_r/tw_v)**2)
    r_slow_rebound_rate_virtual = r_slow_rebound_rate*((tw_r/tw_v)**2)
    r_fast_bump_rate_virtual = r_fast_bump_rate*((tw_r/tw_v)**2)
    r_fast_rebound_rate_virtual = r_fast_rebound_rate*((tw_r/tw_v)**2)

    return(tw_v,
    f_wheel_rate_virtual,
    r_wheel_rate_virtual, 
    f_slow_bump_rate_virtual,
    f_slow_rebound_rate_virtual,
    f_fast_bump_rate_virtual,
    f_fast_rebound_rate_virtual,
    r_slow_bump_rate_virtual,
    r_slow_rebound_rate_virtual,
    r_fast_bump_rate_virtual,
    r_fast_rebound_rate_virtual)