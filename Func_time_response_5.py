import numpy as np
import math

def TimeResponseV(TW_f, TW_r, FmotionRatioWD, RmotionRatioWD, FmotionRatioWS, RmotionRatioWS,
                fSlowBump, rSlowBump, fSlowRebound, rSlowRebound,
                fFastBump, rFastBump, fFastRebound, rFastRebound,
                kneeSpeedFB, kneeSpeedRB, kneeSpeedFR, kneeSpeedRR,
                ARBRateF, ARBRateR, fWheelRate, rWheelRate, aeroLoadF, aeroLoadR,
                fls, frs, rls, rrs, flu, fru, rlu, rru, rotatingInertia,
                
                kT_f, kT_r, tireDiam_f, tireDiam_r, cgHeight, rcHeight_f, rcHeight_r, F, s):
    n=len(F)
    
    #Start Loop Variables
    ddFO = np.ones(n)*fSlowBump
    ddRO = np.ones(n)*rSlowBump
    ddFI = np.ones(n)*fSlowRebound
    ddRI = np.ones(n)*rSlowRebound
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
    
    #Track Widths, Convert to Imperial
    TW_f = TW_f*0.0254
    TW_r = TW_r*0.0254
    TW_x = (TW_f+TW_r)/2
    M = TW_r/TW_f #Converts y_f to y_r or v_f to v_r
    
    #Masses, convert from Imperial (lbs) to Metric (kg)
    weightDist_f = (fls+frs)/(fls+frs+rls+rrs)
    weightDist_r = 1-weightDist_f
    fls=fls/2.20462
    frs=frs/2.20462
    rls=rls/2.20462
    rrs=rrs/2.20462
    flu=flu/2.20462
    fru=fru/2.20462
    rlu=rlu/2.20462
    rru=rru/2.20462
    SM = (fls+frs+rls+rrs)/2
    USM_f = (flu+fru)/2 #average front corner USM
    USM_r = (rlu+rru)/2
    OSM = (rotatingInertia*0.5*(0.0254**2)/2.20462)*((TW_x/2)**2) #Should be ~350/570 of the sprung mass
    #TODO: Check OSM again.
    print(OSM)
    
    ARBRateF = ARBRateF*4.44822/0.0254
    ARBRateR = ARBRateR*4.44822/0.0254
    fWheelRate = fWheelRate*4.44822/0.0254
    rWheelRate = rWheelRate*4.44822/0.0254
    kS_f = fWheelRate + ARBRateF
    kT_f = kT_f*4.44822/0.0254
    cS_f = (ddFO[i] + ddFI[i])/2
    cT_f = kT_f/160 #gamma=0.2 is 1500, hardcoded as a proportion of the kT because so un-knowable to the user? 160:1 is the ratio?
    kS_r = rWheelRate + ARBRateR
    kT_r = kT_r*4.44822/0.0254
    cS_r = (ddRO[i] + ddRI[i])/2
    cT_r = kT_r/160
    aeroLoadF = aeroLoadF*4.44822
    aeroLoadR = aeroLoadR*4.44822

    #Geometry, convert to Metric
    cgHeight = cgHeight*0.0254
    rcHeight_f = rcHeight_f*0.0254
    rcHeight_r = rcHeight_r*0.0254
    rcHeightAtCG = rcHeight_f+weightDist_f*(rcHeight_r-rcHeight_f)
    tireDiam_f = tireDiam_f*0.0254
    tireDiam_r = tireDiam_r*0.0254
    
    #Position and velocity variables. Y suspension travel, V suspension velocity, A tire travel, B tire velocity.
    yNow = 0
    vNow = 0
    aNow_f = 0
    bNow_f = 0
    aNow_r = 0
    bNow_r = 0
    
    #Begin RK4 Loop
    for all in range(n-1):

        #F/T terms are driven by the total static mass, defines the resting position
        T = F[i]*9.80665*SM*(cgHeight-rcHeightAtCG)#(cg-RC)/TW
        TNext = F[i+1]*9.80665*SM*(cgHeight-rcHeightAtCG)#(cg-RC)/TW
        THalfNext = (T+TNext)/2

        #GSMs are completely F/R decoupled.
        Fgsm_f = F[i]*9.80665*SM*weightDist_f*(rcHeight_f/(TW_f/2))#RC/TW
        FgsmNext_f = F[i+1]*9.80665*SM*weightDist_f*(rcHeight_f/(TW_f/2))#RC/TW
        FgsmHalfNext_f = (Fgsm_f+FgsmNext_f)/2

        Fgsm_r = F[i]*9.80665*SM*weightDist_r*(rcHeight_r/(TW_r/2))#RC/TW
        FgsmNext_r = F[i+1]*9.80665*SM*weightDist_r*(rcHeight_r/(TW_r/2))#RC/TW
        FgsmHalfNext_r = (Fgsm_r+FgsmNext_r)/2

        Fgusm_f = F[i]*9.80665*USM_f*(tireDiam_f/(2*TW_f/2))#Tire Width/2
        FgusmNext_f = F[i+1]*9.80665*USM_f*(tireDiam_f/(2*TW_f/2))#Tire Width/2
        FgusmHalfNext_f = (Fgusm_f+FgusmNext_f)/2

        Fgusm_r = F[i]*9.80665*USM_r*(tireDiam_r/(2*TW_r/2))#Tire Width/2
        FgusmNext_r = F[i+1]*9.80665*USM_r*(tireDiam_r/(2*TW_r/2))#Tire Width/2
        FgusmHalfNext_r = (Fgusm_r+FgusmNext_r)/2

        #J,K,C,D terms are divided by OSM or OUSM, which define the frequency of oscillation.
        #"Oscillating" mass and "forcing" mass is therefore decoupled in the roll motion
        j1 = dt*(T - (kS_f*yNow + cS_f*vNow)*TW_f/2 - (kS_r*yNow*M + cS_r*vNow*M)*TW_r/2)/(OSM*TW_x/2)
        k1 = dt*vNow
        d1_f = dt*(Fgsm_f/2 + Fgusm_f/2 + cS_f*vNow + kS_f*yNow - cT_f*bNow_f - kT_f*aNow_f)/USM_f
        c1_f = dt*bNow_f
        d1_r = dt*(Fgsm_r/2 + Fgusm_r/2 + cS_r*vNow*M + kS_r*yNow*M - cT_r*bNow_r - kT_r*aNow_r)/USM_r
        c1_r = dt*bNow_r

        j2 = dt*(THalfNext - (kS_f*(yNow+k1/2) + cS_f*(vNow+j1/2))*TW_f/2 - (kS_r*(yNow+k1/2)*M + cS_r*(vNow+j1/2)*M)*TW_r/2)/(OSM*TW_x/2)
        k2 = dt*(vNow+j1/2)
        d2_f = dt*(FgsmHalfNext_f/2 + FgusmHalfNext_f/2 + cS_f*(vNow+j1/2) + kS_f*(yNow+k1/2) - cT_f*(bNow_f+d1_f/2) - kT_f*(aNow_f+c1_f/2))/USM_f
        c2_f = dt*(bNow_f+d1_f/2)
        d2_r = dt*(FgsmHalfNext_r/2 + FgusmHalfNext_r/2 + cS_r*(vNow+j1/2)*M + kS_r*(yNow+k1/2)*M - cT_r*(bNow_r+d1_r/2) - kT_r*(aNow_r+c1_r/2))/USM_r
        c2_r = dt*(bNow_r+d1_r/2)

        j3 = dt*(THalfNext - (kS_f*(yNow+k2/2) + cS_f*(vNow+j2/2))*TW_f/2 - (kS_r*(yNow+k2/2)*M + cS_r*(vNow+j2/2)*M)*TW_r/2)/(OSM*TW_x/2)
        k3 = dt*(vNow+j2/2)
        d3_f = dt*(FgsmHalfNext_f/2 + FgusmHalfNext_f/2 + cS_f*(vNow+j2/2) + kS_f*(yNow+k2/2) - cT_f*(bNow_f+d2_f/2) - kT_f*(aNow_f+c2_f/2))/USM_f
        c3_f = dt*(bNow_f+d2_f/2)
        d3_r = dt*(FgsmHalfNext_r/2 + FgusmHalfNext_r/2 + cS_r*(vNow+j2/2)*M + kS_r*(yNow+k2/2)*M - cT_r*(bNow_r+d2_r/2) - kT_r*(aNow_r+c2_r/2))/USM_r
        c3_r = dt*(bNow_r+d2_r/2)

        j4 = dt*(TNext - (kS_f*(yNow+k3) + cS_f*(vNow+j3))*TW_f/2 - (kS_r*(yNow+k3)*M + cS_r*(vNow+j3)*M)*TW_r/2)/(OSM*TW_x/2)
        k4 = dt*(vNow+j3)
        d4_f = dt*(FgsmNext_f/2 + FgusmNext_f/2 + cS_f*(vNow+j3) + kS_f*(yNow+k3) - cT_f*(bNow_f+d3_f) - kT_f*(aNow_f+c3_f))/USM_f
        c4_f = dt*(bNow_f+d3_f)
        d4_r = dt*(FgsmNext_r/2 + FgusmNext_r/2 + cS_r*(vNow+j3)*M + kS_r*(yNow+k3)*M - cT_r*(bNow_r+d3_r) - kT_r*(aNow_r+c3_r))/USM_r
        c4_r = dt*(bNow_r+d3_r)

        vNext = vNow + (j1 + 2*j2 + 2*j3 + j4)/6
        yNext = yNow + (k1 + 2*k2 + 2*k3 + k4)/6
        bNext_f = bNow_f + (d1_f + 2*d2_f + 2*d3_f + d4_f)/6
        aNext_f = aNow_f + (c1_f + 2*c2_f + 2*c3_f + c4_f)/6
        bNext_r = bNow_r + (d1_r + 2*d2_r + 2*d3_r + d4_r)/6
        aNext_r = aNow_r + (c1_r + 2*c2_r + 2*c3_r + c4_r)/6

        vNow = vNext
        yNow = yNext
        bNow_f = bNext_f
        aNow_f = aNext_f
        bNow_r = bNext_r
        aNow_r = aNext_r
    
        #Within RK4 Loop...
        #TODO: Define Roll Angle Correctly
        rollAngle[i] = math.atan(yNow/(TW_x/2))*180/math.pi
        wheelDispF[i] = yNow
        wheelDispR[i] = yNow*M
        tireDispF[i] = aNow_f
        tireDispR[i] = aNow_r
        
        damperDispF[i] = wheelDispF[i]/FmotionRatioWD
        damperDispR[i] = wheelDispR[i]/RmotionRatioWD
        springDispF[i] = wheelDispF[i]/FmotionRatioWS
        springDispR[i] = wheelDispR[i]/RmotionRatioWS
        
        if i>0:
            damperVelF[i] = (damperDispF[i]-damperDispF[i-1])/dt #can also be replaced with vNow_f/motion ratio?
            damperVelR[i] = (damperDispR[i]-damperDispR[i-1])/dt
        
        if np.average([damperVelF[i], damperVelR[i]]) >= 0: #If rolling clockwise     
            if damperVelF[i]<=kneeSpeedFB:
                damperForceFO[i] = damperVelF[i]*fSlowBump
                ddFO[i]=fSlowBump
            else:
                damperForceFO[i] = (damperVelF[i]-kneeSpeedFB)*fFastBump+kneeSpeedFB*fSlowBump
                ddFO[i]=fFastBump
            if damperVelR[i]<=kneeSpeedRB:
                damperForceRO[i] = damperVelR[i]*rSlowBump
                ddRO[i]=rSlowBump
            else:
                damperForceRO[i] = (damperVelR[i]-kneeSpeedRB)*rFastBump+kneeSpeedRB*rSlowBump
                ddRO[i]=rFastBump
            if damperVelF[i]<=kneeSpeedFR:
                damperForceFI[i] = damperVelF[i]*fSlowRebound
                ddFI[i]=fSlowRebound
            else:
                damperForceFI[i] = (damperVelF[i]-kneeSpeedFR)*fFastRebound+kneeSpeedFR*fSlowRebound
                ddFI[i]=fFastRebound
            if damperVelR[i]<=kneeSpeedRR:
                damperForceRI[i] = damperVelR[i]*rSlowRebound
                ddRI[i]=rSlowRebound
            else:
                damperForceRI[i] = (damperVelR[i]-kneeSpeedRR)*rFastRebound+kneeSpeedRR*rSlowRebound
                ddRI[i]=rFastRebound
                
        if np.average([damperVelF[i], damperVelR[i]]) < 0: #If rolling counter-clockwise
            if damperVelF[i]<=kneeSpeedFR:
                damperForceFO[i] = damperVelF[i]*fSlowRebound
                ddFO[i]=fSlowRebound
            else:
                damperForceFO[i] = (damperVelF[i]-kneeSpeedFR)*fFastRebound+kneeSpeedFR*fSlowRebound
                ddFO[i]=fFastRebound
            if damperVelR[i]<=kneeSpeedRR:
                damperForceRO[i] = damperVelR[i]*rSlowRebound
                ddRO[i]=rSlowRebound
            else:
                damperForceRO[i] = (damperVelR[i]-kneeSpeedRR)*rFastRebound+kneeSpeedRR*fSlowRebound
                ddRO[i]=rFastRebound
            if damperVelF[i]<=kneeSpeedFB:
                damperForceFI[i] = damperVelF[i]*fSlowBump
                ddFI[i]=fSlowBump
            else:
                damperForceFI[i] = (damperVelF[i]-kneeSpeedFB)*fFastBump+kneeSpeedFB*fSlowBump
                ddFI[i]=fFastBump
            if damperVelR[i]<=kneeSpeedRB:
                damperForceRI[i] = damperVelR[i]*rSlowBump
                ddRI[i]=rSlowBump
            else:
                damperForceRI[i] = (damperVelR[i]-kneeSpeedRB)*rFastBump+kneeSpeedRB*rSlowBump
                ddRI[i]=rFastBump
                
        cS_f = (ddFO[i] + ddFI[i])/2
        cS_r = (ddRO[i] + ddRI[i])/2
        
        if i>0 and i<=n-1: #CHECK TO REDEFINE FREQUENCIES AND DAMP RATIOS_____________________________________________________________________________________
            if ddFO[i] != ddFO[i-1] or ddRO[i] != ddRO[i-1] or ddFI[i] != ddFI[i-1] or ddRI[i] != ddRI[i-1]:
                print('Damper domain changed.')
                print(cS_f, cS_r, i)
        
        #TODO: Aerodynamic loads need to be incorporated into ODEs!!! Maybe next version :)
        #TODO: Consider L/R symmetry and if the symmetric half-model is valid while plugging in asymmetric damper values later.
        #      Might have to have all 4 wheels represented in ODEs.
        #      As of right now, not certain that aNow*kT + bNow*cT is valid to use symmetrically
        tireLoadFO[i] = aNow_f*kT_f + bNow_f*cT_f + aeroLoadF/2 + (fls + flu)*9.80665
        tireLoadRO[i] = aNow_r*kT_r + bNow_r*cT_r + aeroLoadR/2 + (rls + rlu)*9.80665
        tireLoadFI[i] = -(aNow_f*kT_f + bNow_f*cT_f) + aeroLoadF/2 + (frs + fru)*9.80665
        tireLoadRI[i] = -(aNow_r*kT_r + bNow_r*cT_r) + aeroLoadR/2 + (rrs + rru)*9.80665
        frontLLT[i] = (tireLoadFO[i])/(tireLoadFO[i]+tireLoadFI[i])#Use these definitions in basic parameters window too.
        rearLLT[i] = (tireLoadRO[i])/(tireLoadRO[i]+tireLoadRI[i])
        LLTR[i] = frontLLT[i]/rearLLT[i]
        
        i=i+1
    
    print('d1_f:')
    print(Fgsm_f/2 + Fgusm_f/2 + cS_f*vNow + kS_f*yNow - cT_f*bNow_f - kT_f*aNow_f, Fgsm_f, Fgusm_f, cS_f*vNow, kS_f*yNow, cT_f*bNow_f, kT_f*aNow_f)
    print('d2_f:')
    print(FgsmHalfNext_f/2 + FgusmHalfNext_f/2 + cS_f*(vNow+j1/2) + kS_f*(yNow+k1/2) - cT_f*(bNow_f+d1_f/2) - kT_f*(aNow_f+c1_f/2), FgsmHalfNext_f, FgusmHalfNext_f, cS_f*(vNow+j1/2), kS_f*(yNow+k1/2), cT_f*(bNow_f+d1_f/2), kT_f*(aNow_f+c1_f/2))
    print('d3_f:')
    print(FgsmHalfNext_f/2 + FgusmHalfNext_f/2 + cS_f*(vNow+j2/2) + kS_f*(yNow+k2/2) - cT_f*(bNow_f+d2_f/2) - kT_f*(aNow_f+c2_f/2), FgsmHalfNext_f, FgusmHalfNext_f, cS_f*(vNow+j2/2), kS_f*(yNow+k2/2), cT_f*(bNow_f+d2_f/2), kT_f*(aNow_f+c2_f/2))
    print('d4_f:')
    print(FgsmNext_f/2 + FgusmNext_f/2 + cS_f*(vNow+j3) + kS_f*(yNow+k3) - cT_f*(bNow_f+d3_f) - kT_f*(aNow_f+c3_f), FgsmNext_f, FgusmNext_f, cS_f*(vNow+j3), kS_f*(yNow+k3), cT_f*(bNow_f+d3_f), kT_f*(aNow_f+c3_f))
    print(aNow_f, aNow_r, yNow, yNow*M)
    print(' ')
    
    peakRA = str(round(max(rollAngle), 3))
    #overshootRA = str(round(100*(max(rollAngle)-rollAngle)/rollAngle, 1))
    overshootRA = str(0)
    peakfV = str(round(max(damperVelF), 3))
    peakrV = str(round(max(damperVelR), 3))
    peakDampFO = str(round(abs(max(damperForceFO))))
    peakDampRO = str(round(abs(max(damperForceRO))))
    peakDampFI = str(round(abs(max(damperForceFI))))
    peakDampRI = str(round(abs(max(damperForceRI))))
    peakLoadFO = str(round(max(tireLoadFO)))
    peakLoadRO = str(round(max(tireLoadRO)))
    peakfLLT = str(round(100*max(frontLLT), 1))
    peakrLLT = str(round(100*max(rearLLT), 1))
    peakLLTR = str(round(max(LLTR), 3))
    minLLTR = str(round(min(LLTR), 3))
    #overshootfLLT = str(round(100*((100*max(frontLLT))-FWeightTransfer)/FWeightTransfer, 1))
    #overshootrLLT = str(round(100*((100*max(rearLLT))-RWeightTransfer)/RWeightTransfer, 1))
    #overshootLLTR = str(round(((100*max(LLTR))-LLTRvar)/LLTRvar, 3))
    overshootfLLT = str(0)
    overshootrLLT = str(0)
    overshootLLTR = str(0)
    
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