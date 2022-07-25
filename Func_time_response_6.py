import numpy as np
import math
from Func_virtual_track_conversion import *

def RSF_transient_response_VI(F, s):

    n=len(F)

    rollAngle = np.zeros(n)
    wheelDispF = np.zeros(n)
    wheelDispR = np.zeros(n)
    tireDispF = np.zeros(n)
    tireDispR = np.zeros(n)
    damperDispF = np.zeros(n)
    damperDispR = np.zeros(n)
    damperVelF = np.zeros(n)
    damperVelR = np.zeros(n)
    springDispF = np.zeros(n)
    springDispR = np.zeros(n)
    tireLoadFO = np.zeros(n)
    tireLoadFI = np.zeros(n)
    tireLoadRO = np.zeros(n)
    tireLoadRI = np.zeros(n)
    damperForceFO = np.zeros(n)
    damperForceFI = np.zeros(n)
    damperForceRO = np.zeros(n)
    damperForceRI = np.zeros(n)
    frontLLT = np.zeros(n)
    rearLLT = np.zeros(n)
    LLTR = np.zeros(n)

    i=0
    t = np.linspace(-0.1, s, num=n)
    tNow = t[i]
    tNext = t[i+1]
    dt = tNext-tNow
    tHalfNext = tNow+dt/2

    return(t, rollAngle, damperVelF, damperVelR,
           damperForceFO, damperForceFI, damperForceRO, damperForceRI,
           tireLoadFO, tireLoadFI, tireLoadRO, tireLoadRI,
           100*frontLLT, 100*rearLLT, LLTR, #14
           
           peakRA, overshootRA, peakfV, peakrV,
           peakDampFO, peakDampRO, peakDampFI, peakDampRI, #22
           peakLoadFO, peakLoadRO, #24
           peakfLLT, peakrLLT, peakLLTR, #27
           overshootfLLT, overshootrLLT, overshootLLTR, minLLTR, #31
          
           1000*(wheelDispF+tireDispF), 1000*(wheelDispR+tireDispR)) #32, 33