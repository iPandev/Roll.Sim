from math import sqrt, pi

#unsprung mass should say sprung.
def UndampedRideFrequencyCalc(WheelRate, UnsprungCornerMass, WheelRateMod, UnsprungCornerMassMod):
    
    UndampedRideFrequency = (1/(2*pi))*sqrt(WheelRate/(UnsprungCornerMass/(12*32.174)))
    UndampedRideFrequencyMod = (1/(2*pi))*sqrt(WheelRateMod/(UnsprungCornerMassMod/(12*32.174)))
    UndampedRideFrequencyPercent = 100*((UndampedRideFrequencyMod-UndampedRideFrequency)/UndampedRideFrequency)
    UndampedRideFrequencySTR = str(round(UndampedRideFrequency, 3))
    UndampedRideFrequencyModSTR = str(round(UndampedRideFrequencyMod, 3))
    UndampedRideFrequencyPercentSTR = str(round(UndampedRideFrequencyPercent, 1))
    
    return(UndampedRideFrequency,
           UndampedRideFrequencyMod,
           UndampedRideFrequencyPercent,
           UndampedRideFrequencySTR,
           UndampedRideFrequencyModSTR,
           UndampedRideFrequencyPercentSTR
          )