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
    
    #1.UNSPRUNG GEOMETRIC LOAD TRANSFER____________________________________________________________________________________________________________________________________________
    fUnsprungGeoLT = Gforce*9.80665*fUnsprungMass*(tireDiameterF/2)/(TWf) #N
    rUnsprungGeoLT = Gforce*9.80665*rUnsprungMass*(tireDiameterR/2)/(TWr) #new differential of forces, absolute value added to outside wheel is half. This is correct.
    
    #2.SPRUNG GEOMETRIC LOAD TRANSFER______________________________________________________________________________________________________________________________________________
    fSprungGeoLT = Gforce*9.80665*fSprungMass*frcHeight/(TWf) #N
    rSprungGeoLT = Gforce*9.80665*rSprungMass*rrcHeight/(TWr) 
    
    #3.ELASTIC ROLL ANGLE__________________________________________________________________________________________________________________________________________________________
    rcm = frcHeight*(fWeightDist)+rrcHeight*(1-fWeightDist) #m
    elasticRollAngle = math.atan(0.5*Gforce*9.80665*sprungMass*(cmHeight-rcm)/(fCombinedRate*(TWf**2)/4+rCombinedRate*(TWr**2)/4))#in rad
    
    #4.SPRUNG ELASTIC LOAD TRANSFER________________________________________________________________________________________________________________________________________________
    fElasticLT = fCombinedRate*math.tan(elasticRollAngle)*TWf/2 #ABSOLUTE force transferred to outside wheel, this is correct since TWf is halved
    rElasticLT = rCombinedRate*math.tan(elasticRollAngle)*TWr/2
    
    #5.TIRE DEFLECTION_____________________________________________________________________________________________________________________________________________________________
    fTireDeflection = (fUnsprungGeoLT/2 + fSprungGeoLT/2 + fElasticLT)/fTireK
    rTireDeflection = (rUnsprungGeoLT/2 + rSprungGeoLT/2 + rElasticLT)/rTireK
    
    #6.SPRING DEFLECTION___________________________________________________________________________________________________________________________________________________________
    fWheelDeflection = fElasticLT/fCombinedRate
    fWheelDeflectionCheck = math.tan(elasticRollAngle)*TWf/2 #Note the use of elastic roll angle, not total
    rWheelDeflection = rElasticLT/rCombinedRate
    rWheelDeflectionCheck = math.tan(elasticRollAngle)*TWr/2
    
    FSpringTravelFromRest = fWheelDeflection/FMotionRatioWS/.0254
    RSpringTravelFromRest = rWheelDeflection/RMotionRatioWS/.0254
    FDamperTravelFromRest = fWheelDeflection/FMotionRatioDS/.0254
    RDamperTravelFromRest = rWheelDeflection/RMotionRatioDS/.0254
    FSpringTravelFromRestSTR = str(round(FSpringTravelFromRest, 3))
    RSpringTravelFromRestSTR = str(round(RSpringTravelFromRest, 3))
    FDamperTravelFromRestSTR = str(round(FDamperTravelFromRest, 3))
    RDamperTravelFromRestSTR = str(round(RDamperTravelFromRest, 3))
    
    #7A.CHASSIS ROLL ANGLE__________________________________________________________________________________________________________________________________________________________
    ra1 = math.atan(fWheelDeflection/(TWf/2))
    ra2 = math.atan(rWheelDeflection/(TWr/2))
    chassisRollAngle = (ra1+ra2)/2 #rad
    rollAngleDeg = 180*(chassisRollAngle)/math.pi
    rollAngleDegSTR = str(round(rollAngleDeg, 3))
    #totalRollAngleCheck = 
    
    #7B.TOTAL ROLL ANGLE____________________________________________________________________________________________________________________________________________________________
    tra1 = math.atan((fWheelDeflection+fTireDeflection)/(TWf/2))
    tra2 = math.atan((rWheelDeflection+rTireDeflection)/(TWr/2))
    totalRollAngle = (tra1+tra2)/2 #rad
    #rollAngleDeg = 180*(totalRollAngle)/math.pi
    #rollAngleDegSTR = str(round(rollAngleDeg, 3))
    
    #8.COMBINED LOAD TRASNFRS AND LLTR______________________________________________________________________________________________________________________________________________
    fLLT = (100)*((fUnsprungMass+fSprungMass)*9.80665/2 + aeroLoadF/2 + fUnsprungGeoLT/2 + fSprungGeoLT/2 + fElasticLT)/((fUnsprungMass+fSprungMass)*9.80665+aeroLoadF)
    rLLT = (100)*((rUnsprungMass+rSprungMass)*9.80665/2 + aeroLoadR/2 + rUnsprungGeoLT/2 + rSprungGeoLT/2 + rElasticLT)/((rUnsprungMass+rSprungMass)*9.80665+aeroLoadR)
    print(fUnsprungGeoLT, fSprungGeoLT, fElasticLT, fTireDeflection, fWheelDeflection, rTireDeflection, rWheelDeflection)
    LLTR = fLLT/rLLT
    fLLTSTR = str(round(fLLT, 1))
    rLLTSTR = str(round(rLLT, 1))
    LLTRSTR = str(round(LLTR, 3))
    
    #9.NAT ROLL FREQUENCY___________________________________________________________________________________________________________________________________________________________
    rollinertia = rollinertia*0.453592/(39.3701**2)
    virtualInertialMass = rollinertia/(((TWf/2+TWr/2)/2)**2)
    NatRollFreq = (1/(2*math.pi))*math.sqrt((fCombinedRate+rCombinedRate)/(virtualInertialMass/2))
    NatRollFreqSTR = str(round(NatRollFreq, 3))
    
    #INCLUDE OPTIMUM G TECH TIP METHOD AS A CHECK w=1/(2pi)*sqrt(180K/piI)
    
    #10.ROLL DAMP RATIOS____________________________________________________________________________________________________________________________________________________________
    Ccr = 2*math.sqrt((fCombinedRate+rCombinedRate)*virtualInertialMass/2)
    Cs = (damp1 + damp2 + damp3 + damp4)/2
    Cf = (damp5 + damp6 + damp7 + damp8)/2
    dampingRatioSlow = Cs/Ccr
    dampingRatioSlowSTR = str(round(dampingRatioSlow, 3))
    dampingRatioFast = Cf/Ccr
    dampingRatioFastSTR = str(round(dampingRatioFast, 3))
    
    #11.DAMPED ROLL FREQENCY________________________________________________________________________________________________________________________________________________________
    if dampingRatioSlow < 1:
        dampedRollFreqSlow = NatRollFreq*math.sqrt(1-dampingRatioSlow**2)
        dampedRollFreqSlowSTR = str(round(dampedRollFreqSlow, 3))
    else:
        dampedRollFreqSlow = 1
        dampedRollFreqSlowSTR = 'na'
        
    if dampingRatioFast < 1:
        dampedRollFreqFast = NatRollFreq*math.sqrt(1-dampingRatioFast**2)
        dampedRollFreqFastSTR = str(round(dampedRollFreqFast, 3))
    else:
        dampedRollFreqFast = 1
        dampedRollFreqFastSTR = 'na'
    
    return(rollAngleDegSTR, #0
           fLLTSTR, #1
           rLLTSTR, #2
           LLTRSTR, #3
           FSpringTravelFromRestSTR, #4
           RSpringTravelFromRestSTR, #5
           FDamperTravelFromRestSTR, #6
           RDamperTravelFromRestSTR, #7
           rollAngleDeg, #8
           fLLT, #9
           rLLT, #10
           LLTR, #11
           FSpringTravelFromRest, #12
           RSpringTravelFromRest, #13
           FDamperTravelFromRest, #14
           RDamperTravelFromRest, #15
           #
           NatRollFreq, #16
           NatRollFreqSTR, #17
           dampingRatioSlow, #18
           dampingRatioSlowSTR, #19
           dampingRatioFast, #20
           dampingRatioFastSTR, #21
           dampedRollFreqSlow, #22
           dampedRollFreqSlowSTR, #23
           dampedRollFreqFast, #24
           dampedRollFreqFastSTR, #25
           1000*(fWheelDeflection+fTireDeflection), #26
           1000*(rWheelDeflection+rTireDeflection), #27
           #TroubleshootingVars
           Ccr, #28
           fWheelDeflection,
           fWheelDeflectionCheck,
           tra1*180/3.14,
           tra2*180/3.14
          )