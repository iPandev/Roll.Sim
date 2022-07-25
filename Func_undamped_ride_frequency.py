from math import sqrt, pi

def RSF_undamped_ride_freq(WheelRate, SprungCornerMass, WheelRateMod, SprungCornerMassMod):
    
    UndampedRideFrequency = (1/(2*pi))*sqrt(WheelRate/(SprungCornerMass/(12*32.174)))
    UndampedRideFrequencyMod = (1/(2*pi))*sqrt(WheelRateMod/(SprungCornerMassMod/(12*32.174)))
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