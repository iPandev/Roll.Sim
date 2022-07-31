# A function to convert the spring rate and all 4 damper rates of all 4 wheels, to the at-wheel spring rates and at-wheel damper rates calcualted at a virtual track width, which is the average of the front and rear track widths.
#TODO: validate Karb calculations

def RSF_virtual_track(tw_f, tw_r, #track widths
    Ks_f, Ks_r, Karb_f, Karb_r, #coil and anti-roll bar spring rates
    Csb_f, Csr_f, Cfb_f, Cfr_f, #front dampers
    Csb_r, Csr_r, Cfb_r, Cfr_r): #rear dampers

    tw_v = (tw_f + tw_r)/2 #avg track width is virtual track width

    return((tw_f + tw_r)/2, #tw_v
    Ks_f*((tw_f/tw_v)**2), #Ks_f_v
    Ks_r*((tw_r/tw_v)**2), #Ks_r_v
    Karb_f*((tw_f/tw_v)**2), #Karb_f_v
    Karb_r*((tw_r/tw_v)**2), #Karb_r_v
    Csb_f*((tw_f/tw_v)**2), #Csb_f_v
    Csr_f*((tw_f/tw_v)**2), #Csr_f_v 
    Cfb_f*((tw_f/tw_v)**2), #Cfb_f_v
    Cfr_f*((tw_f/tw_v)**2), #Cfr_f_v
    Csb_r*((tw_r/tw_v)**2), #Csb_r_v
    Csr_r*((tw_r/tw_v)**2), #Csr_r_v
    Cfb_r*((tw_r/tw_v)**2), #Cfb_r_v
    Cfr_r*((tw_r/tw_v)**2)) #Cfr_r_v