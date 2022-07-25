def RSF_weight_dist(fl, fr, rl, rr, flMod, frMod, rlMod, rrMod):
    total = fl+fr+rl+rr
    frontDist = 100*(fl+fr)/total
    leftDist = 100*(fl+rl)/total
    cross = 100*(fl+rr)/total
    
    frontDistSTR = str(round(frontDist, 1))
    leftDistSTR =  str(round(leftDist, 1))
    crossSTR = str(round(cross, 1))
    
    totalMod = flMod+frMod+rlMod+rrMod
    frontDistMod = 100*(flMod+frMod)/totalMod
    leftDistMod = 100*(flMod+rlMod)/totalMod
    crossMod = 100*(flMod+rrMod)/totalMod
    
    frontDistModSTR = str(round(frontDistMod, 1))
    leftDistModSTR =  str(round(leftDistMod, 1))
    crossModSTR = str(round(crossMod, 1))
    
    frontDistPercent = 100*((frontDistMod-frontDist)/frontDist)
    leftDistPercent = 100*((leftDistMod-leftDist)/leftDist)
    crossPercent = 100*((crossMod-cross)/cross)
    
    frontDistPercentSTR = str(round(frontDistPercent, 1))
    leftDistPercentSTR =  str(round(leftDistPercent, 1))
    crossPercentSTR = str(round(crossPercent, 1))
    
    return(frontDist, leftDist, cross,
           frontDistMod, leftDistMod, crossMod,
           frontDistPercent, leftDistPercent, crossPercent,
           frontDistSTR, leftDistSTR, crossSTR,
           frontDistModSTR, leftDistModSTR, crossModSTR,
           frontDistPercentSTR, leftDistPercentSTR, crossPercentSTR,
           total, totalMod)