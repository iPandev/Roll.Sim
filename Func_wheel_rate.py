#This function wis valid for both spring or damper rates. Therefore, the variable name "spring rate" is changed to the more general "rate."

def RSF_wheel_rate(Rate, MotionRatioWS, RateMod, MotionRatioWSMod):
    
    WheelRate = Rate/(MotionRatioWS**2)
    WheelRateMod = RateMod/(MotionRatioWSMod**2)
    WheelRatePercent = 100*((WheelRateMod-WheelRate)/WheelRate)
    WheelRateSTR = str(round(WheelRate, 1))
    WheelRateModSTR = str(round(WheelRateMod, 1))
    WheelRatePercentSTR = str(round(WheelRatePercent, 1))
    
    return(WheelRate, WheelRateMod, WheelRatePercent, WheelRateSTR, WheelRateModSTR, WheelRatePercentSTR)