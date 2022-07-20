version = '0.2.0'

#Import Python modules
import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from string import *
from math import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk)
from functools import partial

#Import Roll.Sim functions
from Func_wheel_rate import *
from Func_undamped_ride_frequency import *
from Func_wheel_damping_ratio import *
from Func_weight_dist import *
from Func_steady_state_roll import *
from Func_time_response_5 import *

if __name__ == '__main__':
    print('Welcome to Roll.Sim 0.2.0!')

    safety = Tk()
    safety.title('Roll.Sim 1.10')

    Label1 = Label(safety, wraplength=400, justify="center",
                text="""Roll.Sim 1.10""", font=('bold')).grid(row=0, column=0)

    Label1 = Label(safety, wraplength=400, justify="center",
                text="""Vehicle Response Simulator
    Copyright (C) 2021 Ivan S. Pandev

    Welcome! Roll.Sim is a highly experimental, limited, open-loop, as-yet unvalidated simulator of vehicle behavior, and only for academic purposes, with no guarantee whatsoever of its results correlating to real-world behavior. DO NOT apply changes to real-world vehicles based solely on Roll.Sim results. Doing so can result in damage to property, bodily injury, or death. By using Roll.Sim, you, the user, accept this risk and agree never to hold Roll.Sim’s creators responsible for such damages.

    Please read the complete safety warning and complete liability limitation before continuing by clicking the below buttons.
        """).grid(row=1, column=0)

    def Home():  
        
        root = Tk()
        root.title('Roll.Sim 1.10')

        #Data Gathering

        #FRONT DATA GATHERING

        LabelM = Label(root, text='_______FRONT_______').grid(row=0, column=0)
        LabelM = Label(root, text='Base').grid(row=0, column=1)
        LabelM = Label(root, text='Mod').grid(row=0, column=2)
        LabelM = Label(root, text='     ').grid(row=1, column=0)
        LabelM = Label(root, text='Base').grid(row=0, column=5)
        LabelM = Label(root, text='Mod').grid(row=0, column=6)

        Label1 = Label(root, text="Spring Rate:").grid(row=1,column=0)
        eFSpringRate = Entry(root, width=7)
        eFSpringRate.grid(row=1, column=1)
        eFSpringRate.insert(0, "450")
        eFSpringRateMod = Entry(root, width=7)
        eFSpringRateMod.grid(row=1, column=2)
        eFSpringRateMod.insert(0, "450")
        Label1u = Label(root, text=" lbs/in.").grid(row=1,column=3)

        Label2 = Label(root, text="Wheel:Spring Motion Ratio:").grid(row=2,column=0)
        eFMotionRatioWS = Entry(root, width=7)
        eFMotionRatioWS.grid(row=2, column=1)
        eFMotionRatioWS.insert(0, "1.1")
        eFMotionRatioWSMod = Entry(root, width=7)
        eFMotionRatioWSMod.grid(row=2, column=2)
        eFMotionRatioWSMod.insert(0, "1.1")
        Label2u = Label(root, text=" W:S ").grid(row=2,column=3)

        Label7 = Label(root, text="Wheel:Damper Motion Ratio:").grid(row=3,column=0)
        eFMotionRatioWD = Entry(root, width=7)
        eFMotionRatioWD.grid(row=3, column=1)
        eFMotionRatioWD.insert(0, "1.1")
        eFMotionRatioWDMod = Entry(root, width=7)
        eFMotionRatioWDMod.grid(row=3, column=2)
        eFMotionRatioWDMod.insert(0, "1.1")
        Label7u = Label(root, text=" W:D ").grid(row=3,column=3)

        Label8 = Label(root, text="Damper Rate, Slow Bump:").grid(row=4,column=0)
        eFDamperRateSB = Entry(root, width=7)
        eFDamperRateSB.grid(row=4, column=1)
        eFDamperRateSB.insert(0, "3846.2")
        eFDamperRateSBMod = Entry(root, width=7)
        eFDamperRateSBMod.grid(row=4, column=2)
        eFDamperRateSBMod.insert(0, "3846.2")
        Label8u = Label(root, text=" N/(m/s) ").grid(row=4,column=3)

        Label9 = Label(root, text="Damper Rate, Fast Bump:").grid(row=5,column=0)
        eFDamperRateFB = Entry(root, width=7)
        eFDamperRateFB.grid(row=5, column=1)
        eFDamperRateFB.insert(0, "1000")
        eFDamperRateFBMod = Entry(root, width=7)
        eFDamperRateFBMod.grid(row=5, column=2)
        eFDamperRateFBMod.insert(0, "1000")
        Label9u = Label(root, text=" N/(m/s) ").grid(row=5,column=3)

        Label10 = Label(root, text="Damper Rate, Slow Rebound:").grid(row=6,column=0)
        eFDamperRateSR = Entry(root, width=7)
        eFDamperRateSR.grid(row=6, column=1)
        eFDamperRateSR.insert(0, "6153.0")
        eFDamperRateSRMod = Entry(root, width=7)
        eFDamperRateSRMod.grid(row=6, column=2)
        eFDamperRateSRMod.insert(0, "6153.0")
        Label10u = Label(root, text=" N/(m/s) ").grid(row=6,column=3)

        Label11 = Label(root, text="Damper Rate, Fast Rebound:").grid(row=7,column=0)
        eFDamperRateFR = Entry(root, width=7)
        eFDamperRateFR.grid(row=7, column=1)
        eFDamperRateFR.insert(0, "2500.0")
        eFDamperRateFRMod = Entry(root, width=7)
        eFDamperRateFRMod.grid(row=7, column=2)
        eFDamperRateFRMod.insert(0, "2500.0")
        Label11u = Label(root, text=" N/(m/s) ").grid(row=7,column=3)

        Label12 = Label(root, text="Knee Speed, Bump:").grid(row=8,column=0)
        eFKneeSpeedBump = Entry(root, width=7)
        eFKneeSpeedBump.grid(row=8, column=1)
        eFKneeSpeedBump.insert(0, "0.130")
        eFKneeSpeedBumpMod = Entry(root, width=7)
        eFKneeSpeedBumpMod.grid(row=8, column=2)
        eFKneeSpeedBumpMod.insert(0, "0.130")
        Label12u = Label(root, text=" m/s ").grid(row=8,column=3)

        Label13 = Label(root, text="Knee Speed, Rebound:").grid(row=9,column=0)
        eFKneeSpeedR = Entry(root, width=7)
        eFKneeSpeedR.grid(row=9, column=1)
        eFKneeSpeedR.insert(0, "0.130")
        eFKneeSpeedRMod = Entry(root, width=7)
        eFKneeSpeedRMod.grid(row=9, column=2)
        eFKneeSpeedRMod.insert(0, "0.130")
        Label13u = Label(root, text=" m/s ").grid(row=9,column=3)

        Label14 = Label(root, text="ARB Rate at Wheel:").grid(row=10,column=0)
        eARBRateF = Entry(root, width=7)
        eARBRateF.grid(row=10, column=1)
        eARBRateF.insert(0, "75")
        eARBRateFMod = Entry(root, width=7)
        eARBRateFMod.grid(row=10, column=2)
        eARBRateFMod.insert(0, "75")
        Label14u = Label(root, text=" lbs/in. ").grid(row=10,column=3)

        Label11 = Label(root, text="Roll Center Height:").grid(row=11,column=0)
        eRCHeightF = Entry(root, width=7)
        eRCHeightF.grid(row=11, column=1)
        eRCHeightF.insert(0, "4.0")
        eRCHeightFMod = Entry(root, width=7)
        eRCHeightFMod.grid(row=11, column=2)
        eRCHeightFMod.insert(0, "4.0")
        Label11u = Label(root, text=" in. ").grid(row=11,column=3)

        Label12 = Label(root, text="Tire Stiffness:").grid(row=12,column=0)
        eTireKF = Entry(root, width=7)
        eTireKF.grid(row=12, column=1)
        eTireKF.insert(0, "1720")
        eTireKFMod = Entry(root, width=7)
        eTireKFMod.grid(row=12, column=2)
        eTireKFMod.insert(0, "1720")
        Label12u = Label(root, text=" lbs/in. ").grid(row=12,column=3)
        
        Label13 = Label(root, text="Tire Diameter:").grid(row=13,column=0)
        eTireDF = Entry(root, width=7)
        eTireDF.grid(row=13, column=1)
        eTireDF.insert(0, "23.5")
        eTireDFMod = Entry(root, width=7)
        eTireDFMod.grid(row=13, column=2)
        eTireDFMod.insert(0, "23.5")
        Label13u = Label(root, text=" in. ").grid(row=13,column=3)

        Label14 = Label(root, text="Track Width:").grid(row=14,column=0)
        eFTW = Entry(root, width=7)
        eFTW.grid(row=14, column=1)
        eFTW.insert(0, "60.0")
        eFTWMod = Entry(root, width=7)
        eFTWMod.grid(row=14, column=2)
        eFTWMod.insert(0, "60.0")
        Label14u = Label(root, text=" in. ").grid(row=14,column=3)

        Label15 = Label(root, text="Aerodynamic Load:").grid(row=15,column=0)
        eFAeroLoad = Entry(root, width=7)
        eFAeroLoad.grid(row=15, column=1)
        eFAeroLoad.insert(0, "32")
        eFAeroLoadMod = Entry(root, width=7)
        eFAeroLoadMod.grid(row=15, column=2)
        eFAeroLoadMod.insert(0, "32")
        Label15u = Label(root, text=" lbs ").grid(row=15,column=3)

        #MASSES DATA GATHERING_______________________________________________________________________________________________________

        LabelM = Label(root, text='     ').grid(row=16, column=0)
        LabelM = Label(root, text='_____MASS & INERTIA_____').grid(row=17, column=0)
        LabelM = Label(root, text='Base').grid(row=17, column=1)
        LabelM = Label(root, text='Mod').grid(row=17, column=2)
        LabelM = Label(root, text='Base').grid(row=17, column=5)
        LabelM = Label(root, text='Mod').grid(row=17, column=6)

        Label3 = Label(root, text="FL Corner Total Mass:").grid(row=18,column=0)
        eFLCornerMass = Entry(root, width=7)
        eFLCornerMass.grid(row=18, column=1)
        eFLCornerMass.insert(0, "678")
        eFLCornerMassMod = Entry(root, width=7)
        eFLCornerMassMod.grid(row=18, column=2)
        eFLCornerMassMod.insert(0, "678")
        Label3u = Label(root, text=" lbs").grid(row=18,column=3)

        Label6 = Label(root, text="FL Corner Unsprung Mass:").grid(row=19,column=0)
        eFLCornerUMass = Entry(root, width=7)
        eFLCornerUMass.grid(row=19, column=1)
        eFLCornerUMass.insert(0, "100")
        eFLCornerUMassMod = Entry(root, width=7)
        eFLCornerUMassMod.grid(row=19, column=2)
        eFLCornerUMassMod.insert(0, "100")
        Label6u = Label(root, text=" lbs").grid(row=19,column=3)

        Label4 = Label(root, text="FR Corner Total Mass:").grid(row=18,column=7)
        eFRCornerMass = Entry(root, width=7)
        eFRCornerMass.grid(row=18, column=5)
        eFRCornerMass.insert(0, "657")
        eFRCornerMassMod = Entry(root, width=7)
        eFRCornerMassMod.grid(row=18, column=6)
        eFRCornerMassMod.insert(0, "657")

        Label20 = Label(root, text="FR Corner Unsprung Mass:").grid(row=19,column=7)
        eFRCornerUMass = Entry(root, width=7)
        eFRCornerUMass.grid(row=19, column=5)
        eFRCornerUMass.insert(0, "100")
        eFRCornerUMassMod = Entry(root, width=7)
        eFRCornerUMassMod.grid(row=19, column=6)
        eFRCornerUMassMod.insert(0, "100")

        Label5 = Label(root, text="RL Corner Total Mass:").grid(row=20,column=0)
        eRLCornerMass = Entry(root, width=7)
        eRLCornerMass.grid(row=20, column=1)
        eRLCornerMass.insert(0, "568")
        eRLCornerMassMod = Entry(root, width=7)
        eRLCornerMassMod.grid(row=20, column=2)
        eRLCornerMassMod.insert(0, "568")
        Label5u = Label(root, text=" lbs").grid(row=20,column=3)

        Label21 = Label(root, text="RL Corner Unsprung Mass:").grid(row=21,column=0)
        eRLCornerUMass = Entry(root, width=7)
        eRLCornerUMass.grid(row=21, column=1)
        eRLCornerUMass.insert(0, "120")
        eRLCornerUMassMod = Entry(root, width=7)
        eRLCornerUMassMod.grid(row=21, column=2)
        eRLCornerUMassMod.insert(0, "120")
        Label21u = Label(root, text=" lbs").grid(row=21,column=3)

        Label5 = Label(root, text="RR Corner Total Mass:").grid(row=20,column=7)
        eRRCornerMass = Entry(root, width=7)
        eRRCornerMass.grid(row=20, column=5)
        eRRCornerMass.insert(0, "559")
        eRRCornerMassMod = Entry(root, width=7)
        eRRCornerMassMod.grid(row=20, column=6)
        eRRCornerMassMod.insert(0, "559")

        Label22 = Label(root, text="RR Corner Unsprung Mass:").grid(row=21,column=7)
        eRRCornerUMass = Entry(root, width=7)
        eRRCornerUMass.grid(row=21, column=5)
        eRRCornerUMass.insert(0, "120")
        eRRCornerUMassMod = Entry(root, width=7)
        eRRCornerUMassMod.grid(row=21, column=6)
        eRRCornerUMassMod.insert(0, "120")

        Label23 = Label(root, text=" CM Height: ").grid(row=22,column=0)
        eCMHeight = Entry(root, width=7)
        eCMHeight.grid(row=22, column=1)
        eCMHeight.insert(0, "19.5")
        eCMHeightMod = Entry(root, width=7)
        eCMHeightMod.grid(row=22, column=2)
        eCMHeightMod.insert(0, "19.5")
        Label23u = Label(root, text=" in.").grid(row=22,column=3)

        Label24 = Label(root, text=" Roll Inertia: ").grid(row=23,column=0)
        eRollInertia = Entry(root, width=7)
        eRollInertia.grid(row=23, column=1)
        eRollInertia.insert(0, "1318000")
        eRollInertiaMod = Entry(root, width=7)
        eRollInertiaMod.grid(row=23, column=2)
        eRollInertiaMod.insert(0, "1318000")
        Label24u = Label(root, text=" lbs*in^2").grid(row=23,column=3)

        #REAR DATA GATHERING #VARIABLE NAMES NEED CHANGING__________________________________________________________________________________________________

        LabelM = Label(root, text='_______REAR_______').grid(row=0, column=7)
        LabelM = Label(root, text='Base').grid(row=30, column=1)
        LabelM = Label(root, text='Mod').grid(row=30, column=2)
        LabelM = Label(root, text='     ').grid(row=29, column=0)

        Label31 = Label(root, text="Spring Rate:").grid(row=1,column=7)
        eRSpringRate = Entry(root, width=7)
        eRSpringRate.grid(row=1, column=5)
        eRSpringRate.insert(0, "750")
        eRSpringRateMod = Entry(root, width=7)
        eRSpringRateMod.grid(row=1, column=6)
        eRSpringRateMod.insert(0, "750")

        Label32 = Label(root, text="Wheel:Spring Motion Ratio:").grid(row=2,column=7)
        eRMotionRatioWS = Entry(root, width=7)
        eRMotionRatioWS.grid(row=2, column=5)
        eRMotionRatioWS.insert(0, "1.48")
        eRMotionRatioWSMod = Entry(root, width=7)
        eRMotionRatioWSMod.grid(row=2, column=6)
        eRMotionRatioWSMod.insert(0, "1.48")

        Label33 = Label(root, text="Wheel:Damper Motion Ratio:").grid(row=3,column=7)
        eRMotionRatioWD = Entry(root, width=7)
        eRMotionRatioWD.grid(row=3, column=5)
        eRMotionRatioWD.insert(0, "1.05")
        eRMotionRatioWDMod = Entry(root, width=7)
        eRMotionRatioWDMod.grid(row=3, column=6)
        eRMotionRatioWDMod.insert(0, "1.05")

        Label34 = Label(root, text="Damper Rate, Slow Bump:").grid(row=4,column=7)
        eRDamperRateSB = Entry(root, width=7)
        eRDamperRateSB.grid(row=4, column=5)
        eRDamperRateSB.insert(0, "2384.0")
        eRDamperRateSBMod = Entry(root, width=7)
        eRDamperRateSBMod.grid(row=4, column=6)
        eRDamperRateSBMod.insert(0, "2384.0")

        Label35 = Label(root, text="Damper Rate, Fast Bump:").grid(row=5,column=7)
        eRDamperRateFB = Entry(root, width=7)
        eRDamperRateFB.grid(row=5, column=5)
        eRDamperRateFB.insert(0, "700")
        eRDamperRateFBMod = Entry(root, width=7)
        eRDamperRateFBMod.grid(row=5, column=6)
        eRDamperRateFBMod.insert(0, "700")

        Label36 = Label(root, text="Damper Rate, Slow Rebound:").grid(row=6,column=7)
        eRDamperRateSR = Entry(root, width=7)
        eRDamperRateSR.grid(row=6, column=5)
        eRDamperRateSR.insert(0, "4615.4")
        eRDamperRateSRMod = Entry(root, width=7)
        eRDamperRateSRMod.grid(row=6, column=6)
        eRDamperRateSRMod.insert(0, "4615.4")

        Label37 = Label(root, text="Damper Rate, Fast Rebound:").grid(row=7,column=7)
        eRDamperRateFR = Entry(root, width=7)
        eRDamperRateFR.grid(row=7, column=5)
        eRDamperRateFR.insert(0, "2302.5")
        eRDamperRateFRMod = Entry(root, width=7)
        eRDamperRateFRMod.grid(row=7, column=6)
        eRDamperRateFRMod.insert(0, "2302.5")

        Label38 = Label(root, text="Knee Speed, Bump:").grid(row=8,column=7)
        eRKneeSpeedBump = Entry(root, width=7)
        eRKneeSpeedBump.grid(row=8, column=5)
        eRKneeSpeedBump.insert(0, "0.130")
        eRKneeSpeedBumpMod = Entry(root, width=7)
        eRKneeSpeedBumpMod.grid(row=8, column=6)
        eRKneeSpeedBumpMod.insert(0, "0.130")

        Label39 = Label(root, text="Knee Speed, Rebound:").grid(row=9,column=7)
        eRKneeSpeedR = Entry(root, width=7)
        eRKneeSpeedR.grid(row=9, column=5)
        eRKneeSpeedR.insert(0, "0.130")
        eRKneeSpeedRMod = Entry(root, width=7)
        eRKneeSpeedRMod.grid(row=9, column=6)
        eRKneeSpeedRMod.insert(0, "0.130")

        Label40 = Label(root, text="ARB Rate at Wheel:").grid(row=10,column=7)
        eARBRateR = Entry(root, width=7)
        eARBRateR.grid(row=10, column=5)
        eARBRateR.insert(0, "25")
        eARBRateRMod = Entry(root, width=7)
        eARBRateRMod.grid(row=10, column=6)
        eARBRateRMod.insert(0, "25")

        Label41 = Label(root, text="Roll Center Height:").grid(row=11,column=7)
        eRCHeightR = Entry(root, width=7)
        eRCHeightR.grid(row=11, column=5)
        eRCHeightR.insert(0, "5.0")
        eRCHeightRMod = Entry(root, width=7)
        eRCHeightRMod.grid(row=11, column=6)
        eRCHeightRMod.insert(0, "5.0")

        Label42 = Label(root, text="Tire Stiffness:").grid(row=12,column=7)
        eTireKR = Entry(root, width=7)
        eTireKR.grid(row=12, column=5)
        eTireKR.insert(0, "1720")
        eTireKRMod = Entry(root, width=7)
        eTireKRMod.grid(row=12, column=6)
        eTireKRMod.insert(0, "1720")
        
        Label43 = Label(root, text="Tire Diameter:").grid(row=13,column=7)
        eTireDR = Entry(root, width=7)
        eTireDR.grid(row=13, column=5)
        eTireDR.insert(0, "23.5")
        eTireDRMod = Entry(root, width=7)
        eTireDRMod.grid(row=13, column=6)
        eTireDRMod.insert(0, "23.5")

        Label44 = Label(root, text="Track Width:").grid(row=14,column=7)
        eRTW = Entry(root, width=7)
        eRTW.grid(row=14, column=5)
        eRTW.insert(0, "62.0")
        eRTWMod = Entry(root, width=7)
        eRTWMod.grid(row=14, column=6)
        eRTWMod.insert(0, "62.0")

        Label45 = Label(root, text="Aerodynamic Load:").grid(row=15,column=7)
        eRAeroLoad = Entry(root, width=7)
        eRAeroLoad.grid(row=15, column=5)
        eRAeroLoad.insert(0, "30")
        eRAeroLoadMod = Entry(root, width=7)
        eRAeroLoadMod.grid(row=15, column=6)
        eRAeroLoadMod.insert(0, "30")

        #INPUT G FORCE___________________________________________________________________________________________________________

        LabelM = Label(root, text='___FORCE FUNCTION___').grid(row=30, column=0)

        Label42 = Label(root, text="Duration:").grid(row=51,column=0)
        eSec = Entry(root, width=7)
        eSec.grid(row=51, column=1)
        eSec.insert(0, "0.5")
        Label42u = Label(root, text=" s ").grid(row=51,column=3)
        
        Label41 = Label(root, text="Max Sustained Lateral G:").grid(row=52,column=0)
        eMaxG = Entry(root, width=7)
        eMaxG.grid(row=52, column=1)
        eMaxG.insert(0, "1.4")
        eMaxGMod = Entry(root, width=7)
        eMaxGMod.grid(row=52, column=2)
        eMaxGMod.insert(0, "1.4")
        Label41u = Label(root, text=" 9.8(m/(s^2)) ").grid(row=52,column=3)
        
        Label43 = Label(root, text="Ramp Time:").grid(row=53,column=0)
        eRampT = Entry(root, width=7)
        eRampT.grid(row=53, column=1)
        eRampT.insert(0, "0.15")
        eRampTMod = Entry(root, width=7)
        eRampTMod.grid(row=53, column=2)
        eRampTMod.insert(0, "0.15")
        Label43u = Label(root, text=" s ").grid(row=53,column=3)
        
        Label43 = Label(root, text="Sin Period:").grid(row=54,column=0)
        eSinT = Entry(root, width=7)
        eSinT.grid(row=54, column=1)
        eSinT.insert(0, "0.7")
        eSinTMod = Entry(root, width=7)
        eSinTMod.grid(row=54, column=2)
        eSinTMod.insert(0, "0.7")
        Label43u = Label(root, text=" s ").grid(row=54,column=3)

        #Results==========================================================================================================================================
        def RollSimMain():

            BasicParamWindow = Tk()
            BasicParamWindow.title('Basic Suspension Parameters')

            #Make STRs + FLOATs from all inputs
            #...Front Parameters
            FSpringRate = float(eFSpringRate.get())
            FSpringRateMod = float(eFSpringRateMod.get())
            RSpringRate = float(eRSpringRate.get())
            RSpringRateMod = float(eRSpringRateMod.get())

            FMotionRatioWS = float(eFMotionRatioWS.get())
            FMotionRatioWSMod = float(eFMotionRatioWSMod.get())
            FMotionRatioWD = float(eFMotionRatioWD.get())
            FMotionRatioWDMod = float(eFMotionRatioWDMod.get())
            RMotionRatioWS = float(eRMotionRatioWS.get())
            RMotionRatioWSMod = float(eRMotionRatioWSMod.get())
            RMotionRatioWD = float(eRMotionRatioWD.get())
            RMotionRatioWDMod = float(eRMotionRatioWDMod.get())

            FDamperRateSB = float(eFDamperRateSB.get())
            FDamperRateSBMod = float(eFDamperRateSBMod.get())
            FDamperRateFB = float(eFDamperRateFB.get())
            FDamperRateFBMod = float(eFDamperRateFBMod.get())
            FDamperRateSR = float(eFDamperRateSR.get())
            FDamperRateSRMod = float(eFDamperRateSRMod.get())
            FDamperRateFR = float(eFDamperRateFR.get())
            FDamperRateFRMod = float(eFDamperRateFRMod.get())
            RDamperRateSB = float(eRDamperRateSB.get())
            RDamperRateSBMod = float(eRDamperRateSBMod.get())
            RDamperRateFB = float(eRDamperRateFB.get())
            RDamperRateFBMod = float(eRDamperRateFBMod.get())
            RDamperRateSR = float(eRDamperRateSR.get())
            RDamperRateSRMod = float(eRDamperRateSRMod.get())
            RDamperRateFR = float(eRDamperRateFR.get())
            RDamperRateFRMod = float(eRDamperRateFRMod.get())

            #...Corner Masses
            FLMass = float(eFLCornerMass.get())
            FRMass = float(eFRCornerMass.get())
            RLMass = float(eRLCornerMass.get())
            RRMass = float(eRRCornerMass.get())
            FLUMass = float(eFLCornerUMass.get())
            FRUMass = float(eFRCornerUMass.get())
            RLUMass = float(eRLCornerUMass.get())
            RRUMass = float(eRRCornerUMass.get())
            FLMassMod = float(eFLCornerMassMod.get())
            FRMassMod = float(eFRCornerMassMod.get())
            RLMassMod = float(eRLCornerMassMod.get())
            RRMassMod = float(eRRCornerMassMod.get())
            FLUMassMod = float(eFLCornerUMassMod.get())
            FRUMassMod = float(eFRCornerUMassMod.get())
            RLUMassMod = float(eRLCornerUMassMod.get())
            RRUMassMod = float(eRRCornerUMassMod.get())

            FLSMass = FLMass - FLUMass
            FRSMass = FRMass - FRUMass
            RLSMass = RLMass - RLUMass
            RRSMass = RRMass - RRUMass
            FLSMassMod = FLMassMod - FLUMassMod
            FRSMassMod = FRMassMod - FRUMassMod
            RLSMassMod = RLMassMod - RLUMassMod
            RRSMassMod = RRMassMod - RRUMassMod

            CMHeight = float(eCMHeight.get())
            CMHeightMod = float(eCMHeightMod.get())
            FRCHeight = float(eRCHeightF.get())
            FRCHeightMod = float(eRCHeightFMod.get())
            RRCHeight = float(eRCHeightR.get())
            RRCHeightMod = float(eRCHeightRMod.get())
            #WheelBase = float(eWB.get())
            #WheelBaseMod = float(eWBMod.get())
            TWf = float(eFTW.get())
            TWfMod = float(eFTWMod.get())
            TWr = float(eRTW.get())
            TWrMod = float(eRTWMod.get())
            Gforce = float(eMaxG.get())
            GforceMod = float(eMaxGMod.get())
            
            TireKF = float(eTireKF.get())
            TireKFMod = float(eTireKFMod.get())
            TireKR = float(eTireKR.get())
            TireKRMod = float(eTireKRMod.get())
            TireDF = float(eTireDF.get())
            TireDFMod = float(eTireDFMod.get())
            TireDR = float(eTireDR.get())
            TireDRMod = float(eTireDRMod.get())
            
            ARBRateF = float(eARBRateF.get())
            ARBRateFMod = float(eARBRateFMod.get())
            ARBRateR = float(eARBRateR.get())
            ARBRateRMod = float(eARBRateRMod.get())
            FAeroLoad = float(eFAeroLoad.get())
            FAeroLoadMod = float(eFAeroLoadMod.get())
            RAeroLoad = float(eRAeroLoad.get())
            RAeroLoadMod = float(eRAeroLoadMod.get())

            RollInertia = float(eRollInertia.get())
            RollInertiaMod = float(eRollInertiaMod.get())

            #MAKE ALL "STEADY STATE" CALCULATIONS--------------------------------------------------------------------------------

            #Used For Roll Behavior
            SprungWeightDistResult =  WeightDistCalc(FLSMass, FRSMass, RLSMass, RRSMass, FLSMassMod, FRSMassMod, RLSMassMod, RRSMassMod)
            FSprungWeightDist = SprungWeightDistResult[0]
            FSprungWeightDistMod = SprungWeightDistResult[3]
            TotalSprungMass = SprungWeightDistResult[18]
            TotalSprungMassMod = SprungWeightDistResult[19]

            #Used for Weight Distribution for Results
            WeightDistResult =  WeightDistCalc(FLMass, FRMass, RLMass, RRMass, FLMassMod, FRMassMod, RLMassMod, RRMassMod)

            #FRONT LEFT___________________

            FLWheelRateResult = WheelRateCalc(FSpringRate, FMotionRatioWS, FSpringRateMod, FMotionRatioWSMod)
            FLWheelRate = FLWheelRateResult[0]
            FLWheelRateMod = FLWheelRateResult[1]

            FLUndamperRideFrequencyResult = UndampedRideFrequencyCalc(FLWheelRate, FLSMass, FLWheelRateMod, FLSMassMod)

            FLDampingRatioSBResult = WheelDampingRatioCalc(FLWheelRate, FLSMass,  FDamperRateSB, FMotionRatioWD,
                                                    FLWheelRateMod, FLSMassMod,  FDamperRateSBMod, FMotionRatioWDMod)

            FLDampingRatioFBResult = WheelDampingRatioCalc(FLWheelRate, FLSMass,  FDamperRateFB, FMotionRatioWD,
                                                    FLWheelRateMod, FLSMassMod,  FDamperRateFBMod, FMotionRatioWDMod)

            FLDampingRatioSRResult = WheelDampingRatioCalc(FLWheelRate, FLSMass,  FDamperRateSR, FMotionRatioWD,
                                                    FLWheelRateMod, FLSMassMod,  FDamperRateSRMod, FMotionRatioWDMod)

            FLDampingRatioFRResult = WheelDampingRatioCalc(FLWheelRate, FLSMass,  FDamperRateFR, FMotionRatioWD,
                                                    FLWheelRateMod, FLSMassMod,  FDamperRateFRMod, FMotionRatioWDMod)

            #FRONT RIGHT___________________

            FRWheelRateResult = WheelRateCalc(FSpringRate,FMotionRatioWS,FSpringRateMod, FMotionRatioWSMod)
            FRWheelRate = FRWheelRateResult[0]
            FRWheelRateMod = FRWheelRateResult[1]

            FRUndamperRideFrequencyResult = UndampedRideFrequencyCalc(FRWheelRate, FRSMass, FRWheelRateMod, FRSMassMod)

            FRDampingRatioSBResult = WheelDampingRatioCalc(FRWheelRate, FRSMass,  FDamperRateSB, FMotionRatioWD,
                                                    FRWheelRateMod, FRSMassMod,  FDamperRateSBMod, FMotionRatioWDMod)

            FRDampingRatioFBResult = WheelDampingRatioCalc(FRWheelRate, FRSMass,  FDamperRateFB, FMotionRatioWD,
                                                    FRWheelRateMod, FRSMassMod,  FDamperRateFBMod, FMotionRatioWDMod)

            FRDampingRatioSRResult = WheelDampingRatioCalc(FRWheelRate, FRSMass,  FDamperRateSR, FMotionRatioWD,
                                                    FRWheelRateMod, FRSMassMod,  FDamperRateSRMod, FMotionRatioWDMod)

            FRDampingRatioFRResult = WheelDampingRatioCalc(FRWheelRate, FRSMass,  FDamperRateFR, FMotionRatioWD,
                                                    FRWheelRateMod, FRSMassMod,  FDamperRateFRMod, FMotionRatioWDMod)

            #REAR LEFT___________________

            RLWheelRateResult = WheelRateCalc(RSpringRate, RMotionRatioWS, RSpringRateMod, RMotionRatioWSMod)
            RLWheelRate = RLWheelRateResult[0]
            RLWheelRateMod = RLWheelRateResult[1]

            RLUndamperRideFrequencyResult = UndampedRideFrequencyCalc(RLWheelRate, RLSMass, RLWheelRateMod, RLSMassMod)

            RLDampingRatioSBResult = WheelDampingRatioCalc(RLWheelRate, RLSMass,  RDamperRateSB, RMotionRatioWD,
                                                    RLWheelRateMod, RLSMassMod,  RDamperRateSBMod, RMotionRatioWDMod)

            RLDampingRatioFBResult = WheelDampingRatioCalc(RLWheelRate, RLSMass,  RDamperRateFB, RMotionRatioWD,
                                                    RLWheelRateMod, RLSMassMod,  RDamperRateFBMod, RMotionRatioWDMod)

            RLDampingRatioSRResult = WheelDampingRatioCalc(RLWheelRate, RLSMass,  RDamperRateSR, RMotionRatioWD,
                                                    RLWheelRateMod, RLSMassMod,  RDamperRateSRMod, RMotionRatioWDMod)

            RLDampingRatioFRResult = WheelDampingRatioCalc(RLWheelRate, RLSMass,  RDamperRateFR, RMotionRatioWD,
                                                    RLWheelRateMod, RLSMassMod,  RDamperRateFRMod, RMotionRatioWDMod)

            #REAR RIGHT___________________

            RRWheelRateResult = WheelRateCalc(RSpringRate,RMotionRatioWS,RSpringRateMod, RMotionRatioWSMod)
            RRWheelRate = RRWheelRateResult[0]
            RRWheelRateMod = RRWheelRateResult[1]

            RRUndamperRideFrequencyResult = UndampedRideFrequencyCalc(RRWheelRate, RRSMass, RRWheelRateMod, RRSMassMod)

            RRDampingRatioSBResult = WheelDampingRatioCalc(RRWheelRate, RRSMass,  RDamperRateSB, RMotionRatioWD,
                                                    RRWheelRateMod, RRSMassMod,  RDamperRateSBMod, RMotionRatioWDMod)

            RRDampingRatioFBResult = WheelDampingRatioCalc(RRWheelRate, RRSMass,  RDamperRateFB, RMotionRatioWD,
                                                    RRWheelRateMod, RRSMassMod,  RDamperRateFBMod, RMotionRatioWDMod)

            RRDampingRatioSRResult = WheelDampingRatioCalc(RRWheelRate, RRSMass,  RDamperRateSR, RMotionRatioWD,
                                                    RRWheelRateMod, RRSMassMod,  RDamperRateSRMod, RMotionRatioWDMod)

            RRDampingRatioFRResult = WheelDampingRatioCalc(RRWheelRate, RRSMass,  RDamperRateFR, RMotionRatioWD,
                                                    RRWheelRateMod, RRSMassMod,  RDamperRateFRMod, RMotionRatioWDMod)

            #STEADY STATE ROLL OUTPUTS________________________
            SSRO = SteadyStateRollOutputs(FSprungWeightDist, CMHeight, FRCHeight, RRCHeight,
                                FRWheelRate, RRWheelRate, TotalSprungMass, FLUMass+FRUMass, RLUMass+RRUMass, Gforce, TWf, TWr,
                                ARBRateF, ARBRateR, FMotionRatioWS, RMotionRatioWS, FMotionRatioWD, RMotionRatioWD,
                                FAeroLoad, RAeroLoad, RollInertia,
                                (FDamperRateSB/(FMotionRatioWD**2)), (FDamperRateSR/(FMotionRatioWD**2)), (RDamperRateSB/(RMotionRatioWD**2)), (RDamperRateSR/(RMotionRatioWD**2)),
                                (FDamperRateFB/(FMotionRatioWD**2)), (FDamperRateFR/(FMotionRatioWD**2)), (RDamperRateFB/(RMotionRatioWD**2)), (RDamperRateFR/(RMotionRatioWD**2)),
                                TireDF, TireDR, TireKF, TireKR 
                                    )

            SSROMod = SteadyStateRollOutputs(FSprungWeightDistMod, CMHeightMod, FRCHeightMod, RRCHeightMod,
                                FRWheelRateMod, RRWheelRateMod, TotalSprungMassMod, FLUMassMod+FRUMassMod, RLUMassMod+RRUMassMod, GforceMod, TWfMod, TWrMod,
                                ARBRateFMod, ARBRateRMod, FMotionRatioWSMod, RMotionRatioWSMod, FMotionRatioWDMod, RMotionRatioWDMod,
                                FAeroLoadMod, RAeroLoadMod, RollInertiaMod,
                                (FDamperRateSBMod/(FMotionRatioWDMod**2)), (FDamperRateSRMod/(FMotionRatioWDMod**2)), (RDamperRateSBMod/(RMotionRatioWDMod**2)), (RDamperRateSRMod/(RMotionRatioWDMod**2)),
                                (FDamperRateFBMod/(FMotionRatioWDMod**2)), (FDamperRateFRMod/(FMotionRatioWDMod**2)), (RDamperRateFBMod/(RMotionRatioWDMod**2)), (RDamperRateFRMod/(RMotionRatioWDMod**2)),
                                TireDFMod, TireDRMod, TireKFMod, TireKRMod 
                                    )

            #Display Results___________________________________________________________________________________________________

            SSGSign = Label(BasicParamWindow, text='_____STEADY STATE CORNERING_____').grid(row=71, column=0)
            SSGSign2 = Label(BasicParamWindow, text='(Base/ Mod/ %)').grid(row=71, column=1)


            Result72 = Label(BasicParamWindow, text = ' Front Weight Transfer: ').grid(row=72, column=0)
            Result72B = Label(BasicParamWindow, text = SSRO[1] + '/ ' + SSROMod[1] + '/ ' + str(round(100*(SSROMod[9]-SSRO[9])/SSRO[9], 1))).grid(row=72, column=1)
            Result72C = Label(BasicParamWindow, text = '%').grid(row=72, column=2)
            Result75 = Label(BasicParamWindow, text = ' Rear Weight Transfer: ').grid(row=73, column=0)
            Result75B = Label(BasicParamWindow, text = SSRO[2] + '/ ' + SSROMod[2] + '/ ' + str(round(100*(SSROMod[10]-SSRO[10])/SSRO[10], 1))).grid(row=73, column=1)
            Result75C = Label(BasicParamWindow, text = '%').grid(row=73, column=2)
            Result78 = Label(BasicParamWindow, text = ' F/R Lateral Load Transfer Ratio: ').grid(row=74, column=0)
            Result78B = Label(BasicParamWindow, text = SSRO[3] + '/ ' + SSROMod[3] + '/ ' + str(round(100*(SSROMod[11]-SSRO[11])/SSRO[11], 1))).grid(row=74, column=1)
            Result78C = Label(BasicParamWindow, text = '-/-').grid(row=74, column=2)

            LabelSpace4 = Label(BasicParamWindow, text='     ').grid(row=75, column=0)

            Result79 = Label(BasicParamWindow, text = ' Natural Roll Frequency: ').grid(row=76, column=0)
            Result79B = Label(BasicParamWindow, text = SSRO[17] + '/ ' + SSROMod[17] + '/ ' + str(round(100*(SSROMod[16]-SSRO[16])/SSRO[16], 1))).grid(row=76, column=1)
            Result79C = Label(BasicParamWindow, text = 'hz').grid(row=76, column=2)
            Result80 = Label(BasicParamWindow, text = ' Roll Damping Ratio (Slow): ').grid(row=77, column=0)
            Result80B = Label(BasicParamWindow, text = SSRO[19] + '/ ' + SSROMod[19] + '/ ' + str(round(100*(SSROMod[18]-SSRO[18])/SSRO[18], 1))).grid(row=77, column=1)
            Result80C = Label(BasicParamWindow, text = 'hz').grid(row=77, column=2)
            Result81 = Label(BasicParamWindow, text = ' Roll Damping Ratio (Fast): ').grid(row=78, column=0)
            Result81B = Label(BasicParamWindow, text = SSRO[21] + '/ ' + SSROMod[21] + '/ ' + str(round(100*(SSROMod[20]-SSRO[20])/SSRO[20], 1))).grid(row=78, column=1)
            Result81C = Label(BasicParamWindow, text = 'hz').grid(row=78, column=2)
            Result82 = Label(BasicParamWindow, text = ' Damped Roll Frequency (Slow): ').grid(row=79, column=0)
            Result82B = Label(BasicParamWindow, text = SSRO[23] + '/ ' + SSROMod[23] + '/ ' + str(round(100*(SSROMod[22]-SSRO[22])/SSRO[22], 1))).grid(row=79, column=1)
            Result82C = Label(BasicParamWindow, text = 'hz').grid(row=79, column=2)
            Result83 = Label(BasicParamWindow, text = ' Damped Roll Frequency (Fast): ').grid(row=80, column=0)
            Result83B = Label(BasicParamWindow, text = SSRO[25] + '/ ' + SSROMod[25] + '/ ' + str(round(100*(SSROMod[24]-SSRO[24])/SSRO[24], 1))).grid(row=80, column=1)
            Result83C = Label(BasicParamWindow, text = 'hz').grid(row=80, column=2)

            LabelSpace5 = Label(BasicParamWindow, text='     ').grid(row=81, column=0)

            Result84 = Label(BasicParamWindow, text = ' Roll Angle (About Roll Axis): ').grid(row=82, column=0)
            Result84B = Label(BasicParamWindow, text = SSRO[0] + '/ ' + SSROMod[0] + '/ ' + str(round(100*(SSROMod[8]-SSRO[8])/SSRO[8], 1))).grid(row=82, column=1)
            Result84C = Label(BasicParamWindow, text = 'deg').grid(row=82, column=2)
            Result73 = Label(BasicParamWindow, text = ' Front Spring Defl. from Rest: ').grid(row=83, column=0)
            Result73B = Label(BasicParamWindow, text = SSRO[4] + '/ ' + SSROMod[4] + '/ ' + str(round(100*(SSROMod[12]-SSRO[12])/SSRO[12], 1))).grid(row=83, column=1)
            Result73C = Label(BasicParamWindow, text = 'in.').grid(row=83, column=2)
            Result74 = Label(BasicParamWindow, text = ' Front Damper Defl. from Rest: ').grid(row=84, column=0)
            Result74B = Label(BasicParamWindow, text = SSRO[6] + '/ ' + SSROMod[6] + '/ ' + str(round(100*(SSROMod[14]-SSRO[14])/SSRO[14], 1))).grid(row=84, column=1)
            Result74C = Label(BasicParamWindow, text = 'in.').grid(row=84, column=2)
            Result76 = Label(BasicParamWindow, text = ' Rear Spring Defl. from Rest: ').grid(row=85, column=0)
            Result76B = Label(BasicParamWindow, text = SSRO[5] + '/ ' + SSROMod[5] + '/ ' + str(round(100*(SSROMod[13]-SSRO[13])/SSRO[13], 1))).grid(row=85, column=1)
            Result76C = Label(BasicParamWindow, text = 'in.').grid(row=85, column=2)
            Result77 = Label(BasicParamWindow, text = ' Rear Damper Defl. from Rest: ').grid(row=86, column=0)
            Result77B = Label(BasicParamWindow, text = SSRO[7] + '/ ' + SSROMod[7] + '/ ' + str(round(100*(SSROMod[15]-SSRO[15])/SSRO[15], 1))).grid(row=86, column=1)
            Result77C = Label(BasicParamWindow, text = 'in.').grid(row=86, column=2)

            LabelSpace3 = Label(BasicParamWindow, text='     ').grid(row=99, column=0)

            FLSign = Label(BasicParamWindow, text='_______FL CORNER_______').grid(row=100, column=0)
            FLSign2 = Label(BasicParamWindow, text='(Base/ Mod/ %)').grid(row=100, column=1)
            FRSign = Label(BasicParamWindow, text='_______FR CORNER_______').grid(row=100, column=5)
            FRSign2 = Label(BasicParamWindow, text='(Base/ Mod/ %)').grid(row=100, column=6)

            Result1 = Label(BasicParamWindow, text = ' Wheel Rate: ').grid(row=101, column=0)
            Result1B = Label(BasicParamWindow, text = FLWheelRateResult[3] + '/ ' + FLWheelRateResult[4] + '/ ' + FLWheelRateResult[5]).grid(row=101, column=1)
            Result1C = Label(BasicParamWindow, text = 'lbs/in.').grid(row=101, column=2)

            Result2 = Label(BasicParamWindow, text = ' Undamped Ride Frequency: ').grid(row=102, column=0)
            Result2B = Label(BasicParamWindow, text = FLUndamperRideFrequencyResult[3] + '/ ' + FLUndamperRideFrequencyResult[4] + '/ ' + FLUndamperRideFrequencyResult[5]).grid(row=102, column=1)
            Result2C = Label(BasicParamWindow, text = 'hz').grid(row=102, column=2)

            Result3 = Label(BasicParamWindow, text = ' Damping Ratio, Slow Bump: ').grid(row=103, column=0)
            Result3B = Label(BasicParamWindow, text = FLDampingRatioSBResult[3] + '/ ' + FLDampingRatioSBResult[4] + '/ ' + FLDampingRatioSBResult[5]).grid(row=103, column=1)
            Result3C = Label(BasicParamWindow, text = '-/-').grid(row=103, column=2)

            Result4 = Label(BasicParamWindow, text = ' Damping Ratio, Fast Bump: ').grid(row=104, column=0)
            Result4B = Label(BasicParamWindow, text = FLDampingRatioFBResult[3] + '/ ' + FLDampingRatioFBResult[4] + '/ ' + FLDampingRatioFBResult[5]).grid(row=104, column=1)
            Result4C = Label(BasicParamWindow, text = '-/-').grid(row=104, column=2)

            Result5 = Label(BasicParamWindow, text = ' Damping Ratio, Slow Rebound: ').grid(row=105, column=0)
            Result5B = Label(BasicParamWindow, text = FLDampingRatioSRResult[3] + '/ ' + FLDampingRatioSRResult[4] + '/ ' + FLDampingRatioSRResult[5]).grid(row=105, column=1)
            Result5C = Label(BasicParamWindow, text = '-/-').grid(row=105, column=2)

            Result6 = Label(BasicParamWindow, text = ' Damping Ratio, Fast Rebound: ').grid(row=106, column=0)
            Result6B = Label(BasicParamWindow, text = FLDampingRatioFRResult[3] + '/ ' + FLDampingRatioFRResult[4] + '/ ' + FLDampingRatioFRResult[5]).grid(row=106, column=1)
            Result6C = Label(BasicParamWindow, text = '-/-').grid(row=106, column=2)

            Result7 = Label(BasicParamWindow, text = ' Wheel Rate: ').grid(row=101, column=5)
            Result7B = Label(BasicParamWindow, text = FRWheelRateResult[3] + '/ ' + FRWheelRateResult[4] + '/ ' + FRWheelRateResult[5]).grid(row=101, column=6)
            Result7C = Label(BasicParamWindow, text = 'lbs/in.').grid(row=101, column=7)

            Result8 = Label(BasicParamWindow, text = ' Undamped Ride Frequency: ').grid(row=102, column=5)
            Result8B = Label(BasicParamWindow, text = FRUndamperRideFrequencyResult[3] + '/ ' + FRUndamperRideFrequencyResult[4] + '/ ' + FRUndamperRideFrequencyResult[5]).grid(row=102, column=6)
            Result8C = Label(BasicParamWindow, text = 'hz').grid(row=102, column=7)

            Result9 = Label(BasicParamWindow, text = ' Damping Ratio, Slow Bump: ').grid(row=103, column=5)
            Result9B = Label(BasicParamWindow, text = FRDampingRatioSBResult[3] + '/ ' + FRDampingRatioSBResult[4] + '/ ' + FRDampingRatioSBResult[5]).grid(row=103, column=6)
            Result9C = Label(BasicParamWindow, text = '-/-').grid(row=103, column=7)

            Result10 = Label(BasicParamWindow, text = ' Damping Ratio, Fast Bump: ').grid(row=104, column=5)
            Result10B = Label(BasicParamWindow, text = FRDampingRatioFBResult[3] + '/ ' + FRDampingRatioFBResult[4] + '/ ' + FRDampingRatioFBResult[5]).grid(row=104, column=6)
            Result10C = Label(BasicParamWindow, text = '-/-').grid(row=104, column=7)

            Result11 = Label(BasicParamWindow, text = ' Damping Ratio, Slow Rebound: ').grid(row=105, column=5)
            Result11B = Label(BasicParamWindow, text = FRDampingRatioSRResult[3] + '/ ' + FRDampingRatioSRResult[4] + '/ ' + FRDampingRatioSRResult[5]).grid(row=105, column=6)
            Result11C = Label(BasicParamWindow, text = '-/-').grid(row=105, column=7)

            Result12 = Label(BasicParamWindow, text = ' Damping Ratio, Fast Rebound: ').grid(row=106, column=5)
            Result12B = Label(BasicParamWindow, text = FRDampingRatioFRResult[3] + '/ ' + FRDampingRatioFRResult[4] + '/ ' + FRDampingRatioFRResult[5]).grid(row=106, column=6)
            Result12C = Label(BasicParamWindow, text = '-/-').grid(row=106, column=7)

            LabelSpace = Label(BasicParamWindow, text='     ').grid(row=119, column=0)

            FLSign = Label(BasicParamWindow, text='_______RL CORNER_______').grid(row=120, column=0)
            FLSign2 = Label(BasicParamWindow, text='(Base/ Mod/ %)').grid(row=120, column=1)
            FRSign = Label(BasicParamWindow, text='_______RR CORNER_______').grid(row=120, column=5)
            FRSign2 = Label(BasicParamWindow, text='(Base/ Mod/ %)').grid(row=120, column=6)

            Result13 = Label(BasicParamWindow, text = ' Wheel Rate: ').grid(row=121, column=0)
            Result13B = Label(BasicParamWindow, text = RLWheelRateResult[3] + '/ ' + RLWheelRateResult[4] + '/ ' + RLWheelRateResult[5]).grid(row=121, column=1)
            Result13C = Label(BasicParamWindow, text = 'lbs/in.').grid(row=121, column=2)

            Result14 = Label(BasicParamWindow, text = ' Undamped Ride Frequency: ').grid(row=122, column=0)
            Result14B = Label(BasicParamWindow, text = RLUndamperRideFrequencyResult[3] + '/ ' + RLUndamperRideFrequencyResult[4] + '/ ' + RLUndamperRideFrequencyResult[5]).grid(row=122, column=1)
            Result14C = Label(BasicParamWindow, text = 'hz').grid(row=122, column=2)

            Result15 = Label(BasicParamWindow, text = ' Damping Ratio, Slow Bump: ').grid(row=123, column=0)
            Result15B = Label(BasicParamWindow, text = RLDampingRatioSBResult[3] + '/ ' + RLDampingRatioSBResult[4] + '/ ' + RLDampingRatioSBResult[5]).grid(row=123, column=1)
            Result15C = Label(BasicParamWindow, text = '-/-').grid(row=123, column=2)

            Result16 = Label(BasicParamWindow, text = ' Damping Ratio, Fast Bump: ').grid(row=124, column=0)
            Result16B = Label(BasicParamWindow, text = RLDampingRatioFBResult[3] + '/ ' + RLDampingRatioFBResult[4] + '/ ' + RLDampingRatioFBResult[5]).grid(row=124, column=1)
            Result16C = Label(BasicParamWindow, text = '-/-').grid(row=124, column=2)

            Result17 = Label(BasicParamWindow, text = ' Damping Ratio, Slow Rebound: ').grid(row=125, column=0)
            Result17B = Label(BasicParamWindow, text = RLDampingRatioSRResult[3] + '/ ' + RLDampingRatioSRResult[4] + '/ ' + RLDampingRatioSRResult[5]).grid(row=125, column=1)
            Result17C = Label(BasicParamWindow, text = '-/-').grid(row=125, column=2)

            Result18 = Label(BasicParamWindow, text = ' Damping Ratio, Fast Rebound: ').grid(row=126, column=0)
            Result18B = Label(BasicParamWindow, text = RLDampingRatioFRResult[3] + '/ ' + RLDampingRatioFRResult[4] + '/ ' + RLDampingRatioFRResult[5]).grid(row=126, column=1)
            Result18C = Label(BasicParamWindow, text = '-/-').grid(row=126, column=2)

            Result27 = Label(BasicParamWindow, text = ' Wheel Rate: ').grid(row=121, column=5)
            Result27B = Label(BasicParamWindow, text = RRWheelRateResult[3] + '/ ' + RRWheelRateResult[4] + '/ ' + RRWheelRateResult[5]).grid(row=121, column=6)
            Result27C = Label(BasicParamWindow, text = 'lbs/in.').grid(row=121, column=7)

            Result28 = Label(BasicParamWindow, text = ' Undamped Ride Frequency: ').grid(row=122, column=5)
            Result28B = Label(BasicParamWindow, text = RRUndamperRideFrequencyResult[3] + '/ ' + RRUndamperRideFrequencyResult[4] + '/ ' + RRUndamperRideFrequencyResult[5]).grid(row=122, column=6)
            Result28C = Label(BasicParamWindow, text = 'hz').grid(row=122, column=7)

            Result29 = Label(BasicParamWindow, text = ' Damping Ratio, Slow Bump: ').grid(row=123, column=5)
            Result29B = Label(BasicParamWindow, text = RRDampingRatioSBResult[3] + '/ ' + RRDampingRatioSBResult[4] + '/ ' + RRDampingRatioSBResult[5]).grid(row=123, column=6)
            Result29C = Label(BasicParamWindow, text = '-/-').grid(row=123, column=7)

            Result30 = Label(BasicParamWindow, text = ' Damping Ratio, Fast Bump: ').grid(row=124, column=5)
            Result30B = Label(BasicParamWindow, text = RRDampingRatioFBResult[3] + '/ ' + RRDampingRatioFBResult[4] + '/ ' + RRDampingRatioFBResult[5]).grid(row=124, column=6)
            Result30C = Label(BasicParamWindow, text = '-/-').grid(row=124, column=7)

            Result31 = Label(BasicParamWindow, text = ' Damping Ratio, Slow Rebound: ').grid(row=125, column=5)
            Result31B = Label(BasicParamWindow, text = RRDampingRatioSRResult[3] + '/ ' + RRDampingRatioSRResult[4] + '/ ' + RRDampingRatioSRResult[5]).grid(row=125, column=6)
            Result31C = Label(BasicParamWindow, text = '-/-').grid(row=125, column=7)

            Result32 = Label(BasicParamWindow, text = ' Damping Ratio, Fast Rebound: ').grid(row=126, column=5)
            Result32B = Label(BasicParamWindow, text = RRDampingRatioFRResult[3] + '/ ' + RRDampingRatioFRResult[4] + '/ ' + RRDampingRatioFRResult[5]).grid(row=126, column=6)
            Result32C = Label(BasicParamWindow, text = '-/-').grid(row=126, column=7)

            LabelSpace = Label(BasicParamWindow, text='     ').grid(row=139, column=0)
            MassesSign = Label(BasicParamWindow, text='_______WEIGHT DIST._______').grid(row=140, column=0)
            MassesSign2 = Label(BasicParamWindow, text='(Base/ Mod/ %)').grid(row=140, column=1)

            Result34 = Label(BasicParamWindow, text = ' Front Weight: ').grid(row=141, column=0)
            Result34B = Label(BasicParamWindow, text = WeightDistResult[9] + '/ ' + WeightDistResult[12] + '/ ' + WeightDistResult[15]).grid(row=141, column=1)
            Result34C = Label(BasicParamWindow, text = '%').grid(row=141, column=2)

            Result35 = Label(BasicParamWindow, text = ' Left Weight: ').grid(row=142, column=0)
            Result35B = Label(BasicParamWindow, text = WeightDistResult[10] + '/ ' + WeightDistResult[13] + '/ ' + WeightDistResult[16]).grid(row=142, column=1)
            Result35C = Label(BasicParamWindow, text = '%').grid(row=142, column=2)

            Result36 = Label(BasicParamWindow, text = ' FL+RR Cross-Weight: ').grid(row=143, column=0)
            Result36B = Label(BasicParamWindow, text = WeightDistResult[11] + '/ ' + WeightDistResult[14] + '/ ' + WeightDistResult[17]).grid(row=143, column=1)
            Result36C = Label(BasicParamWindow, text = '%').grid(row=143, column=2)


            BasicParamWindow.mainloop()

        #DAMPER PLOTS==========================================================================================================
        def DamperPlots():

            DamperWindow = Tk()
            DamperWindow.title('Damper Plots (Base, Mod)')
            fig = Figure()

            FDamperRateSB = float(eFDamperRateSB.get())
            FDamperRateSBMod = float(eFDamperRateSBMod.get())
            FDamperRateFB = float(eFDamperRateFB.get())
            FDamperRateFBMod = float(eFDamperRateFBMod.get())
            FDamperRateSR = float(eFDamperRateSR.get())
            FDamperRateSRMod = float(eFDamperRateSRMod.get())
            FDamperRateFR = float(eFDamperRateFR.get())
            FDamperRateFRMod = float(eFDamperRateFRMod.get())
            #
            RDamperRateSB = float(eRDamperRateSB.get())
            RDamperRateSBMod = float(eRDamperRateSBMod.get())
            RDamperRateFB = float(eRDamperRateFB.get())
            RDamperRateFBMod = float(eRDamperRateFBMod.get())
            RDamperRateSR = float(eRDamperRateSR.get())
            RDamperRateSRMod = float(eRDamperRateSRMod.get())
            RDamperRateFR = float(eRDamperRateFR.get())
            RDamperRateFRMod = float(eRDamperRateFRMod.get())
            #
            FKneeSpeedBump = float(eFKneeSpeedBump.get())
            FKneeSpeedBumpMod = float(eFKneeSpeedBumpMod.get())
            FKneeSpeedR = float(eFKneeSpeedR.get())
            FKneeSpeedRMod = float(eFKneeSpeedRMod.get())
            RKneeSpeedBump = float(eRKneeSpeedBump.get())
            RKneeSpeedBumpMod = float(eRKneeSpeedBumpMod.get())
            RKneeSpeedR = float(eRKneeSpeedR.get())
            RKneeSpeedRMod = float(eRKneeSpeedRMod.get())

            X=[0.3, FKneeSpeedR, 0, FKneeSpeedBump, 0.3]
            Y=[-FKneeSpeedR*FDamperRateSR-(0.3-FKneeSpeedR)*FDamperRateFR,
            -FKneeSpeedR*FDamperRateSR,
            0,
            FKneeSpeedBump*FDamperRateSB,
            FKneeSpeedBump*FDamperRateSB+(0.3-FKneeSpeedBump)*FDamperRateFB]

            XMod=[0.3, FKneeSpeedRMod, 0, FKneeSpeedBumpMod, 0.3]
            YMod=[-FKneeSpeedRMod*FDamperRateSRMod-(0.3-FKneeSpeedRMod)*FDamperRateFRMod,
                -FKneeSpeedRMod*FDamperRateSRMod,
                0,
                FKneeSpeedBumpMod*FDamperRateSBMod,
                FKneeSpeedBumpMod*FDamperRateSBMod+(0.3-FKneeSpeedBumpMod)*FDamperRateFBMod]

            RX=[0.3, RKneeSpeedR, 0, RKneeSpeedBump, 0.3]
            RY=[-RKneeSpeedR*RDamperRateSR-(0.3-RKneeSpeedR)*RDamperRateFR,
                -RKneeSpeedR*RDamperRateSR,
                0,
                RKneeSpeedBump*RDamperRateSB,
                RKneeSpeedBump*RDamperRateSB+(0.3-RKneeSpeedBump)*RDamperRateFB]

            RXMod=[0.3, RKneeSpeedRMod, 0, RKneeSpeedBumpMod, 0.3]
            RYMod=[-RKneeSpeedRMod*RDamperRateSRMod-(0.3-RKneeSpeedRMod)*RDamperRateFRMod,
                -RKneeSpeedRMod*RDamperRateSRMod,
                0,
                RKneeSpeedBumpMod*RDamperRateSBMod,
                RKneeSpeedBumpMod*RDamperRateSBMod+(0.3-RKneeSpeedBumpMod)*RDamperRateFBMod]

            fig, (ax1, ax2) = plt.subplots(2, figsize=(7,8))
            fig.suptitle('Damper Plot (N v. m/s), Base and Mod')
            ax1.plot(X, Y, label='Base')
            ax1.plot(XMod, YMod, label='Mod')
            ax1.set_ylabel('N, Front')
            #ax1.set_xticks(np.linspace(0, 0.30, 7))
            #ax1.set_yticks([])
            ax1.grid()
            leg = ax1.legend()
            ax2.plot(RX, RY, label = 'Base')
            ax2.plot(RXMod, RYMod, label = 'Mod')
            ax2.set_ylabel('N, Rear')
            ax2.grid()
            leg2 = ax2.legend()

            canvas = FigureCanvasTkAgg(fig, master = DamperWindow)   
            canvas.draw() 
            canvas.get_tk_widget().pack()

            DamperWindow.mainloop()

        #STEP RESPONSE WINDOW________________________________________________________________________________________________
        def Resp3(f_type):

            StepWin = Tk()
            StepWin.title('Roll Step Response, Lateral G (Base, Mod)')
            fig = Figure()

            FSpringRate = float(eFSpringRate.get())
            FSpringRateMod = float(eFSpringRateMod.get())
            RSpringRate = float(eRSpringRate.get())
            RSpringRateMod = float(eRSpringRateMod.get())

            FMotionRatioWS = float(eFMotionRatioWS.get())
            FMotionRatioWSMod = float(eFMotionRatioWSMod.get())
            FMotionRatioWD = float(eFMotionRatioWD.get())
            FMotionRatioWDMod = float(eFMotionRatioWDMod.get())
            RMotionRatioWS = float(eRMotionRatioWS.get())
            RMotionRatioWSMod = float(eRMotionRatioWSMod.get())
            RMotionRatioWD = float(eRMotionRatioWD.get())
            RMotionRatioWDMod = float(eRMotionRatioWDMod.get())

            FDamperRateSB = float(eFDamperRateSB.get())
            FDamperRateSBMod = float(eFDamperRateSBMod.get())
            FDamperRateFB = float(eFDamperRateFB.get())
            FDamperRateFBMod = float(eFDamperRateFBMod.get())
            FDamperRateSR = float(eFDamperRateSR.get())
            FDamperRateSRMod = float(eFDamperRateSRMod.get())
            FDamperRateFR = float(eFDamperRateFR.get())
            FDamperRateFRMod = float(eFDamperRateFRMod.get())
            RDamperRateSB = float(eRDamperRateSB.get())
            RDamperRateSBMod = float(eRDamperRateSBMod.get())
            RDamperRateFB = float(eRDamperRateFB.get())
            RDamperRateFBMod = float(eRDamperRateFBMod.get())
            RDamperRateSR = float(eRDamperRateSR.get())
            RDamperRateSRMod = float(eRDamperRateSRMod.get())
            RDamperRateFR = float(eRDamperRateFR.get())
            RDamperRateFRMod = float(eRDamperRateFRMod.get())

            FKneeSpeedBump = float(eFKneeSpeedBump.get())
            FKneeSpeedBumpMod = float(eFKneeSpeedBumpMod.get())
            FKneeSpeedR = float(eFKneeSpeedR.get())
            FKneeSpeedRMod = float(eFKneeSpeedRMod.get())
            RKneeSpeedBump = float(eRKneeSpeedBump.get())
            RKneeSpeedBumpMod = float(eRKneeSpeedBumpMod.get())
            RKneeSpeedR = float(eRKneeSpeedR.get())
            RKneeSpeedRMod = float(eRKneeSpeedRMod.get())

            #...Corner Masses
            FLMass = float(eFLCornerMass.get())
            FRMass = float(eFRCornerMass.get())
            RLMass = float(eRLCornerMass.get())
            RRMass = float(eRRCornerMass.get())
            FLUMass = float(eFLCornerUMass.get())
            FRUMass = float(eFRCornerUMass.get())
            RLUMass = float(eRLCornerUMass.get())
            RRUMass = float(eRRCornerUMass.get())
            FLMassMod = float(eFLCornerMassMod.get())
            FRMassMod = float(eFRCornerMassMod.get())
            RLMassMod = float(eRLCornerMassMod.get())
            RRMassMod = float(eRRCornerMassMod.get())
            FLUMassMod = float(eFLCornerUMassMod.get())
            FRUMassMod = float(eFRCornerUMassMod.get())
            RLUMassMod = float(eRLCornerUMassMod.get())
            RRUMassMod = float(eRRCornerUMassMod.get())

            FLSMass = FLMass - FLUMass
            FRSMass = FRMass - FRUMass
            RLSMass = RLMass - RLUMass
            RRSMass = RRMass - RRUMass
            FLSMassMod = FLMassMod - FLUMassMod
            FRSMassMod = FRMassMod - FRUMassMod
            RLSMassMod = RLMassMod - RLUMassMod
            RRSMassMod = RRMassMod - RRUMassMod

            CMHeight = float(eCMHeight.get())
            CMHeightMod = float(eCMHeightMod.get())
            FRCHeight = float(eRCHeightF.get())
            FRCHeightMod = float(eRCHeightFMod.get())
            RRCHeight = float(eRCHeightR.get())
            RRCHeightMod = float(eRCHeightRMod.get())
            #WheelBase = float(eWB.get())
            #WheelBaseMod = float(eWBMod.get())
            TWf = float(eFTW.get())
            TWfMod = float(eFTWMod.get())
            TWr = float(eRTW.get())
            TWrMod = float(eRTWMod.get())
            Gforce = float(eMaxG.get())
            GforceMod = float(eMaxGMod.get())
            
            ARBRateF = float(eARBRateF.get())
            ARBRateFMod = float(eARBRateFMod.get())
            ARBRateR = float(eARBRateR.get())
            ARBRateRMod = float(eARBRateRMod.get())
            FAeroLoad = float(eFAeroLoad.get())
            FAeroLoadMod = float(eFAeroLoadMod.get())
            RAeroLoad = float(eRAeroLoad.get())
            RAeroLoadMod = float(eRAeroLoadMod.get())
            
            TireKF = float(eTireKF.get())
            TireKFMod = float(eTireKFMod.get())
            TireKR = float(eTireKR.get())
            TireKRMod = float(eTireKRMod.get())
            TireDF = float(eTireDF.get())
            TireDFMod = float(eTireDFMod.get())
            TireDR = float(eTireDR.get())
            TireDRMod = float(eTireDRMod.get())

            RollInertia = float(eRollInertia.get())
            RollInertiaMod = float(eRollInertiaMod.get())
            
            s = float(eSec.get())
            rampT = float(eRampT.get())
            rampTMod = float(eRampTMod.get())
            p = float(eSinT.get())
            pMod = float(eSinTMod.get())

            FRWheelRateResult = WheelRateCalc(FSpringRate,FMotionRatioWS,FSpringRateMod, FMotionRatioWSMod)
            FRWheelRate = FRWheelRateResult[0]
            FRWheelRateMod = FRWheelRateResult[1]

            RRWheelRateResult = WheelRateCalc(RSpringRate,RMotionRatioWS,RSpringRateMod, RMotionRatioWSMod)
            RRWheelRate = RRWheelRateResult[0]
            RRWheelRateMod = RRWheelRateResult[1]

            SprungWeightDistResult =  WeightDistCalc(FLSMass, FRSMass, RLSMass, RRSMass, FLSMassMod, FRSMassMod, RLSMassMod, RRSMassMod)
            FSprungWeightDist = SprungWeightDistResult[0]
            FSprungWeightDistMod = SprungWeightDistResult[3]
            TotalSprungMass = SprungWeightDistResult[18]
            TotalSprungMassMod = SprungWeightDistResult[19]

            SSRO = SteadyStateRollOutputs(FSprungWeightDist, CMHeight, FRCHeight, RRCHeight,
                                FRWheelRate, RRWheelRate, TotalSprungMass, FLUMass+FRUMass, RLUMass+RRUMass, Gforce, TWf, TWr,
                                ARBRateF, ARBRateR, FMotionRatioWS, RMotionRatioWS, FMotionRatioWD, RMotionRatioWD,
                                FAeroLoad, RAeroLoad, RollInertia,
                                (FDamperRateSB/(FMotionRatioWD**2)), (FDamperRateSR/(FMotionRatioWD**2)), (RDamperRateSB/(RMotionRatioWD**2)), (RDamperRateSR/(RMotionRatioWD**2)),
                                (FDamperRateFB/(FMotionRatioWD**2)), (FDamperRateFR/(FMotionRatioWD**2)), (RDamperRateFB/(RMotionRatioWD**2)), (RDamperRateFR/(RMotionRatioWD**2)),
                                TireDF, TireDR, TireKF, TireKR 
                                    )

            SSROMod = SteadyStateRollOutputs(FSprungWeightDistMod, CMHeightMod, FRCHeightMod, RRCHeightMod,
                                FRWheelRateMod, RRWheelRateMod, TotalSprungMassMod, FLUMassMod+FRUMassMod, RLUMassMod+RRUMassMod, GforceMod, TWfMod, TWrMod,
                                ARBRateFMod, ARBRateRMod, FMotionRatioWSMod, RMotionRatioWSMod, FMotionRatioWDMod, RMotionRatioWDMod,
                                FAeroLoadMod, RAeroLoadMod, RollInertiaMod,
                                (FDamperRateSBMod/(FMotionRatioWDMod**2)), (FDamperRateSRMod/(FMotionRatioWDMod**2)), (RDamperRateSBMod/(RMotionRatioWDMod**2)), (RDamperRateSRMod/(RMotionRatioWDMod**2)),
                                (FDamperRateFBMod/(FMotionRatioWDMod**2)), (FDamperRateFRMod/(FMotionRatioWDMod**2)), (RDamperRateFBMod/(RMotionRatioWDMod**2)), (RDamperRateFRMod/(RMotionRatioWDMod**2)),
                                TireDFMod, TireDRMod, TireKFMod, TireKRMod 
                                    )
            
            segments=10*(0.1+s) #how many 0.1s segments are there?
            n=10000
            
            if f_type == 1:
                F = np.zeros(n)
                start = int(round(n/segments, 0))
                F[start:n] = Gforce
                F_mod = np.zeros(n)
                F_mod[start:n] = GforceMod
            elif f_type == 2:
                F = np.zeros(n)
                start = int(round(n/segments, 0))
                ramp = int(round((rampT*10+1)*n/segments, 0))
                F[start:ramp] = np.linspace(0, Gforce, abs(start-ramp))
                F[ramp:n] = Gforce
                F_mod = np.zeros(n)
                rampMod = int(round((rampTMod*10+1)*n/segments, 0))
                F_mod[start:rampMod] = np.linspace(0, GforceMod, abs(start-rampMod))
                F_mod[rampMod:n] = GforceMod
            elif f_type == 3:
                F = np.zeros(n)
                start = int(round(n/segments, 0))
                F[start:n] = Gforce*np.sin(np.linspace(0, np.pi*2*p, abs(start-n)))
                F_mod = np.zeros(n)
                F_mod[start:n] = GforceMod*np.sin(np.linspace(0, np.pi*2*pMod, abs(start-n)))
            
            #BIG TODO: we need to under stand if we're feeding in at-damper damper rates, or at-wheel damper rates.
            stepResults = TimeResponseV(TWf, TWr,
                        FMotionRatioWD, RMotionRatioWD, FMotionRatioWS, RMotionRatioWS,
                        FDamperRateSB, RDamperRateSB, FDamperRateSR, RDamperRateSR,
                        FDamperRateFB, RDamperRateFB, FDamperRateFR, RDamperRateFR,
                        FKneeSpeedBump, RKneeSpeedBump, FKneeSpeedR, RKneeSpeedR,
                        ARBRateF, ARBRateR, FRWheelRate, RRWheelRate, FAeroLoad, RAeroLoad,
                        FLSMass, FRSMass, RLSMass, RRSMass, FLUMass, FRUMass, RLUMass, RRUMass, RollInertia,
                        TireKF, TireKR, TireDF, TireDR, CMHeight, FRCHeight, RRCHeight, F, s)

            stepResultsMod = TimeResponseV(TWfMod, TWrMod,
                        FMotionRatioWDMod, RMotionRatioWDMod, FMotionRatioWSMod, RMotionRatioWSMod,
                        FDamperRateSBMod, RDamperRateSBMod, FDamperRateSRMod, RDamperRateSRMod,
                        FDamperRateFBMod, RDamperRateFBMod, FDamperRateFRMod, RDamperRateFRMod,
                        FKneeSpeedBumpMod, RKneeSpeedBumpMod, FKneeSpeedRMod, RKneeSpeedRMod,
                        ARBRateFMod, ARBRateRMod, FRWheelRateMod, RRWheelRateMod, FAeroLoadMod, RAeroLoadMod,
                        FLSMassMod, FRSMassMod, RLSMassMod, RRSMassMod, FLUMassMod, FRUMassMod, RLUMassMod, RRUMassMod, RollInertiaMod,
                        TireKFMod, TireKRMod, TireDFMod, TireDRMod, CMHeightMod, FRCHeightMod, RRCHeightMod, F_mod, s)

            fig2, ([[ax0, ax1, ax2, ax3], [ax4, ax5, ax6, ax7]]) = plt.subplots(nrows=2, ncols=4, figsize=(20,11))
            fig2.suptitle('Lateral G Step Response (0-500ms)')

            x = len(stepResults[1])-1
            
            ax0.plot(stepResults[0][0:x], F[0:x], label='Base')
            ax0.plot(stepResults[0][0:x], F_mod[0:x], label='Mod')
            #ax1.plot(XMod, YMod, label='Mod')
            ax0.set_ylabel('Lateral Force Function (G)')
            ax0.set_xlabel('(Max Values); Base:' + str(Gforce) + '/ Mod:' + str(GforceMod))
            ax0.grid()
            leg = ax0.legend()
            
            ax1.plot(stepResults[0][0:x], stepResults[1][0:x], label='Base')
            ax1.plot(stepResultsMod[0][0:x], stepResultsMod[1][0:x], label='Mod')
            ax1.plot(stepResults[0][0:x], SSRO[8]*np.ones(x), label='Control, Base')
            ax1.plot(stepResultsMod[0][0:x], SSROMod[8]*np.ones(x), label='Control, Mod')
            #ax1.plot(XMod, YMod, label='Mod')
            ax1.set_ylabel('Roll Angle (deg)')
            ax1.set_xlabel('(Max Values); Base:' + stepResults[15] + '/ Mod:' + stepResultsMod[15] +
                        '\n (Overshoot %); Base:' + str(round(100*max(stepResults[1])/SSRO[8]-100,1)) + '/ Mod:' + str(round(100*max(stepResultsMod[1])/SSROMod[8]-100,1)) +
                        '\n (Error %); Base' + str(round(100*(SSRO[8]-stepResults[1][x-1])/SSRO[8],3)) + '/ Mod' + str(round(100*(SSROMod[8]-stepResultsMod[1][x-1])/SSROMod[8],3)))
            ax1.grid()
            leg = ax1.legend()
            
            print((SSRO[8]-stepResults[1][x-1])/SSRO[8])
            
            ax2.plot(stepResults[0][0:x], stepResults[32][0:x], label='Front, Base')
            ax2.plot(stepResults[0][0:x], stepResults[33][0:x], label='Rear, Base')
            ax2.plot(stepResultsMod[0][0:x], stepResultsMod[32][0:x], label='Front, Mod')
            ax2.plot(stepResultsMod[0][0:x], stepResultsMod[33][0:x], label='Rear, Mod')
            ax2.plot(stepResults[0][0:x], SSRO[26]*np.ones(x), label='Control, Base Front')
            ax2.plot(stepResults[0][0:x], SSRO[27]*np.ones(x), label='Control, Base Rear')
            ax2.plot(stepResultsMod[0][0:x], SSROMod[26]*np.ones(x), label='Control, Mod Front')
            ax2.plot(stepResultsMod[0][0:x], SSROMod[27]*np.ones(x), label='Control, Mod Rear')
            #ax1.plot(XMod, YMod, label='Mod')
            ax2.set_ylabel('Combined Wheel and Tire Motion (mm)')
            ax2.set_xlabel('(Max Values); Front, Base:' + str(round(max(stepResults[32]),1)) + '/ Rear, Base:' + str(round(max(stepResults[33]),1)) +
                        '/ \n Front, Mod:' + str(round(max(stepResultsMod[32]),1)) +'/ Rear, Mod:' + str(round(max(stepResultsMod[33]),1)))
            ax2.grid()
            leg = ax2.legend(loc=4)

            ax3.plot(stepResults[0], stepResults[2], label = 'Front, Base')
            ax3.plot(stepResults[0], stepResults[3], label = 'Rear, Base')
            ax3.plot(stepResultsMod[0], stepResultsMod[2], label = 'Front, Mod')
            ax3.plot(stepResultsMod[0], stepResultsMod[3], label = 'Rear, Mod')
            ax3.set_ylabel('Outside Damper Speed (m/s)')
            ax3.set_xlabel('(Max Values); Front, Base:' + stepResults[17] + '/ Rear, Base:' + stepResults[18] +
                        '/ \n Front, Mod:' + stepResultsMod[17] +'/ Rear, Mod:' + stepResultsMod[18])
            ax3.grid()
            leg2 = ax3.legend()

            ax4.plot(stepResults[0], stepResults[4], label = 'Front Outside, Base')
            ax4.plot(stepResults[0], -stepResults[5], label = 'Front Inside, Base')
            ax4.plot(stepResults[0], stepResults[6], label = 'Rear Outside, Base')
            ax4.plot(stepResults[0], -stepResults[7], label = 'Rear Inside, Base')
            ax4.plot(stepResultsMod[0], stepResultsMod[4], label = 'Front Outside, Mod')
            ax4.plot(stepResultsMod[0], -stepResultsMod[5], label = 'Front Inside, Mod')
            ax4.plot(stepResultsMod[0], stepResultsMod[6], label = 'Rear Outside, Mod')
            ax4.plot(stepResultsMod[0], -stepResultsMod[7], label = 'Rear Inside, Mod')
            ax4.set_ylabel('Damper Force (N)')
            ax4.set_xlabel('(Max Values); Front Outside, Base:' + stepResults[19] + '/ Front Inside, Base:' + stepResults[21] +
                        '/ \n Rear Outside, Base:'  + stepResults[20] + '/ Rear Inside, Base:' + stepResults[22] +
                        '/ \n Front Outisde, Mod:' + stepResultsMod[19] +'/ Front Inside, Mod:' + stepResultsMod[21] +
                        '/ \n Rear Outside, Mod:'  + stepResultsMod[20] + '/ Rear Inside, Mod:' + stepResultsMod[22])
            ax4.grid()
            leg3 = ax4.legend()

            ax5.plot(stepResults[0][0:x], stepResults[8][0:x], label = 'Front Outside, Base')
            ax5.plot(stepResults[0][0:x], stepResults[9][0:x], label = 'Front Inside, Base')
            ax5.plot(stepResults[0][0:x], stepResults[10][0:x], label = 'Rear Outside, Base')
            ax5.plot(stepResults[0][0:x], stepResults[11][0:x], label = 'Rear Inside, Base')
            ax5.plot(stepResultsMod[0][0:x], stepResultsMod[8][0:x], label = 'Front Outside, Mod')
            ax5.plot(stepResultsMod[0][0:x], stepResultsMod[9][0:x], label = 'Front Inside, Mod')
            ax5.plot(stepResultsMod[0][0:x], stepResultsMod[10][0:x], label = 'Rear Outside, Mod')
            ax5.plot(stepResultsMod[0][0:x], stepResultsMod[11][0:x], label = 'Rear Inside, Mod')
            ax5.set_ylabel('Tire Load (N)')
            ax5.set_xlabel('(Max Values); Front, Base:' + stepResults[23] + '/ Rear, Base:' + stepResults[24] +
                        '/ \n Front, Mod:' + stepResultsMod[23] +'/ Rear, Mod:' + stepResultsMod[24])
            ax5.grid()
            leg4 = ax5.legend(loc=7)

            ax6.plot(stepResults[0][0:x], stepResults[12][0:x], label = 'Front, Base')
            ax6.plot(stepResults[0][0:x], stepResults[13][0:x], label = 'Rear, Base')
            ax6.plot(stepResultsMod[0][0:x], stepResultsMod[12][0:x], label = 'Front, Mod')
            ax6.plot(stepResultsMod[0][0:x], stepResultsMod[13][0:x], label = 'Rear, Mod')
            ax6.plot(stepResultsMod[0][0:x], SSRO[9]*np.ones(x), label='Control, Front Base')
            ax6.plot(stepResultsMod[0][0:x], SSROMod[9]*np.ones(x), label='Control, Front Mod')
            ax6.plot(stepResultsMod[0][0:x], SSRO[10]*np.ones(x), label='Control, Rear Base')
            ax6.plot(stepResultsMod[0][0:x], SSROMod[10]*np.ones(x), label='Control, Rear Mod')
            ax6.set_ylabel('Lateral Load Transfer (%)')
            ax6.set_xlabel('(Max Values); Front, Base:' + stepResults[25] + '/ Rear, Base:' + stepResults[26] +
                        '/ \n Front, Mod:' + stepResultsMod[25] +'/ Rear, Mod:' + stepResultsMod[26] +
                        '\n (Overshoot %); Front, Base:' + str(round(100*max(stepResults[12]-50)/(SSRO[9]-50)-100,1)) + '/ Rear, Base:' + str(round(100*max(stepResults[13]-50)/(SSRO[10]-50)-100,1)) +
                        '\n Front, Mod:' + str(round(100*max(stepResultsMod[12]-50)/(SSROMod[9]-50)-100,1)) + '/ Rear, Mod:' + str(round(100*max(stepResultsMod[13]-50)/(SSROMod[10]-50)-100,1)))
            ax6.grid()
            leg5 = ax6.legend(loc=4)

            ax7.plot(stepResults[0][0:x], stepResults[14][0:x], label='Base')
            ax7.plot(stepResultsMod[0][0:x], stepResultsMod[14][0:x], label='Mod')
            ax7.plot(stepResultsMod[0][0:x], SSRO[11]*np.ones(x), label='Control, Base')
            ax7.plot(stepResultsMod[0][0:x], SSROMod[11]*np.ones(x), label='Control, Mod')
            ax7.set_ylabel('Lateral Load Transfer Ratio')
            ax7.set_xlabel('(Max Values); Base:' + str(round(max(stepResults[14]),3)) + '/ Mod:' + str(round(max(stepResultsMod[14]),3)) +
                        '\n (Min Values); Base:' + str(round(min(stepResults[14][0:x]),3)) + '/ Mod:' + str(round(min(stepResultsMod[14][0:x]),3)) +
                        '\n (Error %); Base' + str(round(100*(SSRO[11]-stepResults[14][x-1])/SSRO[11],3)) + '/ Mod' + str(round(100*(SSROMod[11]-stepResultsMod[14][x-1])/SSROMod[11],3)))
            ax7.grid()
            leg6 = ax7.legend()

            canvas = FigureCanvasTkAgg(fig2, master = StepWin)   
            canvas.draw() 
            canvas.get_tk_widget().pack()

            StepWin.mainloop()

        #BUTTONS=================================================================================================================
        LabelM = Label(root, text='     ')
        LabelM.grid(row=94, column=4)

        DamperPlotButton = Button(root, fg='blue', text = "User Guide", width=16)
        DamperPlotButton.grid(row=131, column=0)

        DamperPlotButton = Button(root, fg='blue', command = DamperPlots , text = "Damper Plots", width=16)
        DamperPlotButton.grid(row=132, column=0)

        CalculateButton = Button(root, text='Basic Parameters', command=RollSimMain, fg='blue', width=16)
        CalculateButton.grid(row=133, column=0)

        DamperPlotButton = Button(root, fg='blue', text = "Roll Response (Step)", command = lambda: Resp3(1), width=16)
        DamperPlotButton.grid(row=134, column=0)

        DamperPlotButton = Button(root, fg='blue', text = "Roll Response (Ramp)", command = lambda: Resp3(2), width=16)
        DamperPlotButton.grid(row=135, column=0)
        
        DamperPlotButton = Button(root, fg='blue', text = "Roll Response (Sin)", command = lambda: Resp3(3), width=16)
        DamperPlotButton.grid(row=136, column=0)

        LabelM = Label(root, text='     ').grid(row=137, column=0)
        
        root.mainloop()

    def S():
        safetyWarning = Tk()
        safetyWarning.title('Safety Warning')
        
        Label3 = Label(safetyWarning, wraplength=400, justify="left",
                text="""
        Do not apply changes to real-world vehicles based solely on Roll.Sim results. Doing so can result in damage to property, bodily injury, or death.
                
        Roll.Sim is for academic purposes only, highly experimental, and not at all production-reday. It is a limited, open-loop, as-yet unvalidated simulator of vehicle behavior, with no guarantee whatsoever of its results correlating to real-world behavior. It is limited in the sense that it can only consider lateral G-force inputs, with constant longitudinal or vertical G-force (assumed as 0.0 and 1.0, respectively), and the vehicle model assumes a perfectly flat surface. It is open-loop in that it cannot accept any corrective feedback from sensors. Finally, it is unvalidated in that it has not yet been vetted by industry professionals, or had its outputs compared to measured real-world outputs for identical inputs.
        
        Roll.Sim uses simplified vehicle models and idealized inputs, as well. These simplifications include, but are not limited to:
        
        -Constant spring- and damper-to-wheel motion ratios
        -Jacking force ares ignored, although this shouldn’t be confused with sprung mass geometric weight transfer which is included in the calculations
        -Small-angle trigonometric assumptions
        -Ignored chassis compliance
        -Constant tire spring and damping rates
        
        As a result of all the above, there are many areas where Roll.Sim outputs might differ from real-world behavior.
        
        Other factors affecting vehicle stability and safety of use which Roll.Sim does not consider at all include, but are not limited to:
        
        -Tire dimensions, temperature, and pressure
        -Tire compound and slip angle curve
        -Wheel alignment
        -Road and track surface conditions, including water, ice, CURBS, BURMS, BUMPS, or painted surfaces.
        -Tire load distribution and its effect on weight transfer (via jacking forces).

        When engineering the chassis and suspension settings for your vehicle, make sure to refer to trusted sources and consider your drivers’ limitations.
        """).grid(row=0, column=0)

        safetyWarning.mainloop

    def LL():
        LL = Tk()
        LL.title('Release of Liability')
        
        Label3 = Label(LL, wraplength=400, justify="left",
                text="""
        TERMS AND CONDITIONS
        
        0. Definitions.
    Each user of Roll.Sim, whether working individually or contributing to a company, including owners and operators of vehicles simulated in Roll.Sim, is addressed as “YOU.”

    Roll.Sim and its creator(s) are addressed as “RELEASEES.”

        1. Disclaimer of Warranty.
    THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY APPLICABLE LAW. EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM “AS IS” WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM IS WITH YOU. SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION.
        
        2. Limitation of Liability.
    IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING WILL ANY COPYRIGHT HOLDER BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS), EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
        
        3. Release of Liability
    YOU hereby release Roll.Sim and its creators and all other persons (hereinafter “RELEASEES”), from any and all liability to you or to your personal representatives, heirs, next of kin and assigns, for and and all loss or damage on account of any injury to your person or property or resulting in your death arising out of or related in any way from using Roll.Sim. This GENERAL RELEASE expressly releases RELEASEES, from injuries and damages that are caused by negligence (whether active or passive, ordinary or gross), or otherwise. This RELEASE is intended to be as broad and inclusive as permitted under California law. If any portion of this RELEASE is held invalid, it is agreed that the balance of the RELEASE shall continue in force and effect.

        4. Interpretation of Sections 1 and 2.
    If the disclaimer of warranty and limitation of liability provided above cannot be given local legal effect according to their terms, reviewing courts shall apply local law that most closely approximates an absolute waiver of all civil liability in connection with the Program, unless a warranty or assumption of liability accompanies a copy of the Program in return for a fee.

        END OF TERMS AND CONDITIONS
        """).grid(row=0, column=0)
        
        LL.mainloop
        
    SButton = Button(safety, command=S, text = """Safety Warning""", width=16)
    SButton.grid(row=5, column=0)

    LLButton = Button(safety, command=LL, text = """Release of Liability""", width=16)
    LLButton.grid(row=7, column=0)

    Label3 = Label(safety, wraplength=400, justify="center",
                text=""" """).grid(row=8, column=0)

    Label3 = Label(safety, wraplength=400, justify="center",
                text="""By clicking the button below and continuing to Roll.Sim, you, the user, certify that you have carefully read, understood, and agree to the Release of Liability Statement and Safety Warning of your own free will.""").grid(row=9, column=0)

    Label3 = Label(safety, wraplength=400, justify="center",
                text=""" """).grid(row=12, column=0)

    HomeButton = Button(safety, command=Home, wraplength=250, fg='white', bg='red', text = """I have read, understand, and agree to the safety warning and release of liability above.""")
    HomeButton.grid(row=11, column=0)

    safety.mainloop()