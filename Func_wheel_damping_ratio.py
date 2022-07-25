from math import sqrt

#NEEDS SOME CONVERSION USING DAMPER:WHEEL MR. NEEDS VALIDATION
def RSF_corner_damping_ratio(WheelRate, SprungMass, DamperRate, WDMR, WheelRateMod, SprungMassMod, DamperRateMod, WDMRMod):
    WheelRateMet = WheelRate/0.005859
    SprungMassMet = SprungMass*0.453592
    CriticalDampingRate = 2*sqrt(WheelRateMet*SprungMassMet)
    WheelDampingRatio = (DamperRate/CriticalDampingRate)/(WDMR**2)
    WheelDampingRatioSTR = str(round(WheelDampingRatio, 3))
    
    WheelRateMetMod = WheelRateMod/0.005859
    SprungMassMetMod = SprungMassMod*0.453592
    CriticalDampingRateMod = 2*sqrt(WheelRateMetMod*SprungMassMetMod)
    WheelDampingRatioMod = (DamperRateMod/CriticalDampingRateMod)/(WDMRMod**2)
    WheelDampingRatioModSTR = str(round(WheelDampingRatioMod, 3))
    
    WheelDampingRatioPercent = 100*((WheelDampingRatioMod-WheelDampingRatio)/WheelDampingRatio)
    WheelDampingRatioPercentSTR = str(round(WheelDampingRatioPercent, 1))
    
    return(WheelDampingRatio,
           WheelDampingRatioMod,
           WheelDampingRatioPercent,
           WheelDampingRatioSTR,
           WheelDampingRatioModSTR,
           WheelDampingRatioPercentSTR)