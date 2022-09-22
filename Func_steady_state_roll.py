#TODO: This part of Roll.Rim needs a serious refactor to be consistent with the EQS of motion that define the Roll.Sim model.

import math

def RSF_steady_state(
    fWeightDist, cmHeight, frcHeight, rrcHeight,
    fWheelRate, rWheelRate, sprungMass, fUnsprungMass, rUnsprungMass, Gforce, TWf, TWr,
    ARBRateF, ARBRateR, FMotionRatioWS, RMotionRatioWS, FMotionRatioDS, RMotionRatioDS,
    aeroLoadF, aeroLoadR,
    rollinertia,
    damp1, damp2, damp3, damp4, damp5, damp6, damp7, damp8,
    tireDiameterF, tireDiameterR, fTireK, rTireK
):

    fWeightDist = fWeightDist/100
    cmHeight = cmHeight*0.0254
    frcHeight = frcHeight*0.0254
    rrcHeight = rrcHeight*0.0254
    sprungMass = sprungMass/2.20462
    fSprungMass = fWeightDist*sprungMass
    rSprungMass = (1-fWeightDist)*sprungMass
    fUnsprungMass = fUnsprungMass/2.20462
    rUnsprungMass = rUnsprungMass/2.20462
    
    fWheelRate = fWheelRate*4.44822/0.0254
    rWheelRate = rWheelRate*4.44822/0.0254
    ARBRateF = ARBRateF*4.44822/0.0254
    ARBRateR = ARBRateR*4.44822/0.0254
    fTireK = fTireK*4.44822/0.0254
    rTireK = rTireK*4.44822/0.0254
    fCombinedRate = (fWheelRate+ARBRateF)
    rCombinedRate = (rWheelRate+ARBRateR)
    
    aeroLoadF = aeroLoadF*4.44822
    aeroLoadR = aeroLoadR*4.44822
    TWf = TWf*0.0254
    TWr = TWr*0.0254
    tireDiameterF = tireDiameterF*0.0254
    tireDiameterR = tireDiameterR*0.0254
    
    #1.UNSPRUNG GEOMETRIC LOAD TRANSFER
    fUnsprungGeoLT = Gforce*9.80665*fUnsprungMass*(tireDiameterF/2)/(TWf) #N
    rUnsprungGeoLT = Gforce*9.80665*rUnsprungMass*(tireDiameterR/2)/(TWr) #N Absolute value added to outside wheel.
    
    #2.SPRUNG GEOMETRIC LOAD TRANSFER
    fSprungGeoLT = Gforce*9.80665*fSprungMass*frcHeight/(TWf) #N
    rSprungGeoLT = Gforce*9.80665*rSprungMass*rrcHeight/(TWr) 
    
    #3.ELASTIC ROLL ANGLE
    rcm = frcHeight*(fWeightDist)+rrcHeight*(1-fWeightDist) #m
    elasticRollAngle = math.atan(0.5*Gforce*9.80665*sprungMass*(cmHeight-rcm)/(fCombinedRate*(TWf**2)/4+rCombinedRate*(TWr**2)/4))#in rad
    
    #4.SPRUNG ELASTIC LOAD TRANSFER
    fElasticLT = fCombinedRate*math.tan(elasticRollAngle)*TWf/2 #ABSOLUTE force transferred to outside wheel, this is correct since TWf is halved
    rElasticLT = rCombinedRate*math.tan(elasticRollAngle)*TWr/2
    
    #5.TIRE DEFLECTION
    fTireDeflection = (fUnsprungGeoLT/2 + fSprungGeoLT/2 + fElasticLT)/fTireK
    rTireDeflection = (rUnsprungGeoLT/2 + rSprungGeoLT/2 + rElasticLT)/rTireK
    
    #6.SPRING DEFLECTION
    fWheelDeflection = fElasticLT/fCombinedRate
    fWheelDeflectionCheck = math.tan(elasticRollAngle)*TWf/2 #Note the use of elastic roll angle, not total
    rWheelDeflection = rElasticLT/rCombinedRate
    rWheelDeflectionCheck = math.tan(elasticRollAngle)*TWr/2
    
    FSpringTravelFromRest = fWheelDeflection/FMotionRatioWS/.0254
    RSpringTravelFromRest = rWheelDeflection/RMotionRatioWS/.0254
    FDamperTravelFromRest = fWheelDeflection/FMotionRatioDS/.0254
    RDamperTravelFromRest = rWheelDeflection/RMotionRatioDS/.0254
    
    #7A.CHASSIS ROLL ANGLE
    ra1 = math.atan(fWheelDeflection/(TWf/2))
    ra2 = math.atan(rWheelDeflection/(TWr/2))
    chassisRollAngle = (ra1+ra2)/2 #rad
    rollAngleDeg = 180*(chassisRollAngle)/math.pi
    
    #7B.TOTAL ROLL ANGLE
    tra1 = math.atan((fWheelDeflection+fTireDeflection)/(TWf/2))
    tra2 = math.atan((rWheelDeflection+rTireDeflection)/(TWr/2))
    totalRollAngle = (tra1+tra2)/2 #rad
    #rollAngleDeg = 180*(totalRollAngle)/math.pi
    #rollAngleDegSTR = str(round(rollAngleDeg, 3))
    
    #8.COMBINED LOAD TRASNFRS AND LLTR
    LLT_f = (100)*((fUnsprungMass+fSprungMass)*9.80665/2 + aeroLoadF/2 + fUnsprungGeoLT/2 + fSprungGeoLT/2 + fElasticLT)/((fUnsprungMass+fSprungMass)*9.80665+aeroLoadF)
    LLT_r = (100)*((rUnsprungMass+rSprungMass)*9.80665/2 + aeroLoadR/2 + rUnsprungGeoLT/2 + rSprungGeoLT/2 + rElasticLT)/((rUnsprungMass+rSprungMass)*9.80665+aeroLoadR)
    LLT_ratio = LLT_f/LLT_r
    
    #9.NAT ROLL FREQUENCY
    rollinertia = rollinertia*0.453592/(39.3701**2)
    virtualInertialMass = rollinertia/(((TWf/2+TWr/2)/2)**2)
    NatRollFreq = (1/(2*math.pi))*math.sqrt((fCombinedRate+rCombinedRate)/(virtualInertialMass/2))
    
    #INCLUDE OPTIMUM G TECH TIP METHOD AS A CHECK w=1/(2pi)*sqrt(180K/piI)
    
    #10.ROLL DAMP RATIOS
    Ccr = 2*math.sqrt((fCombinedRate+rCombinedRate)*virtualInertialMass/2)
    Cs = (damp1 + damp2 + damp3 + damp4)/2
    Cf = (damp5 + damp6 + damp7 + damp8)/2
    dampingRatioSlow = Cs/Ccr
    dampingRatioFast = Cf/Ccr
    
    #11.DAMPED ROLL FREQENCY
    if dampingRatioSlow < 1:
        dampedRollFreqSlow = NatRollFreq*math.sqrt(1-dampingRatioSlow**2)
    else:
        dampedRollFreqSlow = 1
        
    if dampingRatioFast < 1:
        dampedRollFreqFast = NatRollFreq*math.sqrt(1-dampingRatioFast**2)
    else:
        dampedRollFreqFast = 1
    
    return(
        rollAngleDeg, #0
        LLT_f, #1
        LLT_r, #2
        LLT_ratio, #3
        FSpringTravelFromRest, #12, 4
        RSpringTravelFromRest, #13, 5
        FDamperTravelFromRest, #14, 6
        RDamperTravelFromRest, #15, 7
        NatRollFreq, #16, 8
        dampingRatioSlow, #18, 9
        dampingRatioFast, #20, 10
        dampedRollFreqSlow, #22, 11
        dampedRollFreqFast, #24, 12
        1000*(fWheelDeflection+fTireDeflection), #26, 13
        1000*(rWheelDeflection+rTireDeflection), #27, 14
    )