version = '0.3.0'

#Import Python modules
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#Import Roll.Sim functions
from Class_unit_value_pair import UnitValuePair
from Func_wheel_rate import RSF_wheel_rate
from Func_undamped_ride_frequency import RSF_undamped_ride_freq
from Func_wheel_damping_ratio import RSF_corner_damping_ratio
from Func_weight_dist import RSF_weight_dist
from Func_steady_state_roll import RSF_steady_state
from Func_time_response_6 import RSF_transient_response_6

if __name__ == '__main__':
    print(f'Welcome to Roll.Sim {version}!')

    safety = tk.Tk()
    safety.title(f'Roll.Sim {version}')

    tk.Label(safety, wraplength=400, justify="center",
                text=f"""Roll.Sim {version}""", font=('bold')).grid(row=0, column=0)

    tk.Label(safety, wraplength=400, justify="center",
                text="""Vehicle Response Simulator
    Copyright (C) 2022 Ivan S. Pandevs

    Welcome! Roll.Sim is a highly experimental, limited, open-loop, as-yet unvalidated simulator of vehicle behavior, and only for academic purposes, with no guarantee whatsoever of its results correlating to real-world behavior. DO NOT apply changes to real-world vehicles based solely on Roll.Sim results. Doing so can result in damage to property, bodily injury, or death. By using Roll.Sim, you, the user, accept this risk and agree never to hold Roll.Sim’s creators responsible for such damages.

    Please read the complete safety warning and complete liability limitation before continuing by clicking the below buttons.
        """).grid(row=1, column=0)

    def Home():
        
        root = tk.Tk()
        root.title(f'Roll.Sim {version}')

        #FRONT DATA GATHERING

        tk.Label(root, text='_______FRONT_______').grid(row=0, column=0)
        tk.Label(root, text='Base').grid(row=0, column=1)
        tk.Label(root, text='Mod').grid(row=0, column=2)
        tk.Label(root, text='     ').grid(row=1, column=0)
        tk.Label(root, text='Base').grid(row=0, column=5)
        tk.Label(root, text='Mod').grid(row=0, column=6)

        tk.Label(root, text="Spring Rate:").grid(row=1,column=0)
        eFSpringRate = tk.Entry(root, width=7)
        eFSpringRate.grid(row=1, column=1)
        eFSpringRate.insert(0, "450")
        eFSpringRateMod = tk.Entry(root, width=7)
        eFSpringRateMod.grid(row=1, column=2)
        eFSpringRateMod.insert(0, "450")
        tk.Label(root, text=" lbs/in.").grid(row=1,column=3)

        tk.Label(root, text="Wheel:Spring Motion Ratio:").grid(row=2,column=0)
        eFMotionRatioWS = tk.Entry(root, width=7)
        eFMotionRatioWS.grid(row=2, column=1)
        eFMotionRatioWS.insert(0, "1.1")
        eFMotionRatioWSMod = tk.Entry(root, width=7)
        eFMotionRatioWSMod.grid(row=2, column=2)
        eFMotionRatioWSMod.insert(0, "1.1")
        tk.Label(root, text=" W:S ").grid(row=2,column=3)

        tk.Label(root, text="Wheel:Damper Motion Ratio:").grid(row=3,column=0)
        eFMotionRatioWD = tk.Entry(root, width=7)
        eFMotionRatioWD.grid(row=3, column=1)
        eFMotionRatioWD.insert(0, "1.1")
        eFMotionRatioWDMod = tk.Entry(root, width=7)
        eFMotionRatioWDMod.grid(row=3, column=2)
        eFMotionRatioWDMod.insert(0, "1.1")
        tk.Label(root, text=" W:D ").grid(row=3,column=3)

        tk.Label(root, text="Damper Rate, Slow Bump:").grid(row=4,column=0)
        eFDamperRateSB = tk.Entry(root, width=7)
        eFDamperRateSB.grid(row=4, column=1)
        eFDamperRateSB.insert(0, "3846.2")
        eFDamperRateSBMod = tk.Entry(root, width=7)
        eFDamperRateSBMod.grid(row=4, column=2)
        eFDamperRateSBMod.insert(0, "3846.2")
        tk.Label(root, text=" N/(m/s) ").grid(row=4,column=3)

        tk.Label(root, text="Damper Rate, Fast Bump:").grid(row=5,column=0)
        eFDamperRateFB = tk.Entry(root, width=7)
        eFDamperRateFB.grid(row=5, column=1)
        eFDamperRateFB.insert(0, "1000")
        eFDamperRateFBMod = tk.Entry(root, width=7)
        eFDamperRateFBMod.grid(row=5, column=2)
        eFDamperRateFBMod.insert(0, "1000")
        tk.Label(root, text=" N/(m/s) ").grid(row=5,column=3)

        tk.Label(root, text="Damper Rate, Slow Rebound:").grid(row=6,column=0)
        eFDamperRateSR = tk.Entry(root, width=7)
        eFDamperRateSR.grid(row=6, column=1)
        eFDamperRateSR.insert(0, "6153.0")
        eFDamperRateSRMod = tk.Entry(root, width=7)
        eFDamperRateSRMod.grid(row=6, column=2)
        eFDamperRateSRMod.insert(0, "6153.0")
        tk.Label(root, text=" N/(m/s) ").grid(row=6,column=3)

        tk.Label(root, text="Damper Rate, Fast Rebound:").grid(row=7,column=0)
        eFDamperRateFR = tk.Entry(root, width=7)
        eFDamperRateFR.grid(row=7, column=1)
        eFDamperRateFR.insert(0, "2500.0")
        eFDamperRateFRMod = tk.Entry(root, width=7)
        eFDamperRateFRMod.grid(row=7, column=2)
        eFDamperRateFRMod.insert(0, "2500.0")
        tk.Label(root, text=" N/(m/s) ").grid(row=7,column=3)

        tk.Label(root, text="Knee Speed, Bump:").grid(row=8,column=0)
        eFKneeSpeedBump = tk.Entry(root, width=7)
        eFKneeSpeedBump.grid(row=8, column=1)
        eFKneeSpeedBump.insert(0, "0.130")
        eFKneeSpeedBumpMod = tk.Entry(root, width=7)
        eFKneeSpeedBumpMod.grid(row=8, column=2)
        eFKneeSpeedBumpMod.insert(0, "0.130")
        tk.Label(root, text=" m/s ").grid(row=8,column=3)

        tk.Label(root, text="Knee Speed, Rebound:").grid(row=9,column=0)
        eFKneeSpeedR = tk.Entry(root, width=7)
        eFKneeSpeedR.grid(row=9, column=1)
        eFKneeSpeedR.insert(0, "0.130")
        eFKneeSpeedRMod = tk.Entry(root, width=7)
        eFKneeSpeedRMod.grid(row=9, column=2)
        eFKneeSpeedRMod.insert(0, "0.130")
        tk.Label(root, text=" m/s ").grid(row=9,column=3)

        tk.Label(root, text="ARB Rate at Wheel:").grid(row=10,column=0)
        eARBRateF = tk.Entry(root, width=7)
        eARBRateF.grid(row=10, column=1)
        eARBRateF.insert(0, "75")
        eARBRateFMod = tk.Entry(root, width=7)
        eARBRateFMod.grid(row=10, column=2)
        eARBRateFMod.insert(0, "75")
        tk.Label(root, text=" lbs/in. ").grid(row=10,column=3)

        tk.Label(root, text="Roll Center Height:").grid(row=11,column=0)
        eRCHeightF = tk.Entry(root, width=7)
        eRCHeightF.grid(row=11, column=1)
        eRCHeightF.insert(0, "4.0")
        eRCHeightFMod = tk.Entry(root, width=7)
        eRCHeightFMod.grid(row=11, column=2)
        eRCHeightFMod.insert(0, "4.0")
        tk.Label(root, text=" in. ").grid(row=11,column=3)

        tk.Label(root, text="Tire Stiffness:").grid(row=12,column=0)
        eTireKF = tk.Entry(root, width=7)
        eTireKF.grid(row=12, column=1)
        eTireKF.insert(0, "1720")
        eTireKFMod = tk.Entry(root, width=7)
        eTireKFMod.grid(row=12, column=2)
        eTireKFMod.insert(0, "1720")
        tk.Label(root, text=" lbs/in. ").grid(row=12,column=3)
        
        tk.Label(root, text="Tire Diameter:").grid(row=13,column=0)
        eTireDF = tk.Entry(root, width=7)
        eTireDF.grid(row=13, column=1)
        eTireDF.insert(0, "23.5")
        eTireDFMod = tk.Entry(root, width=7)
        eTireDFMod.grid(row=13, column=2)
        eTireDFMod.insert(0, "23.5")
        tk.Label(root, text=" in. ").grid(row=13,column=3)

        tk.Label(root, text="Track Width:").grid(row=14,column=0)
        eFTW = tk.Entry(root, width=7)
        eFTW.grid(row=14, column=1)
        eFTW.insert(0, "60.0")
        eFTWMod = tk.Entry(root, width=7)
        eFTWMod.grid(row=14, column=2)
        eFTWMod.insert(0, "60.0")
        tk.Label(root, text=" in. ").grid(row=14,column=3)

        tk.Label(root, text="Aerodynamic Load:").grid(row=15,column=0)
        eFAeroLoad = tk.Entry(root, width=7)
        eFAeroLoad.grid(row=15, column=1)
        eFAeroLoad.insert(0, "32")
        eFAeroLoadMod = tk.Entry(root, width=7)
        eFAeroLoadMod.grid(row=15, column=2)
        eFAeroLoadMod.insert(0, "32")
        tk.Label(root, text=" lbs ").grid(row=15,column=3)

        #MASSES DATA GATHERING_______________________________________________________________________________________________________

        tk.Label(root, text='     ').grid(row=16, column=0)
        tk.Label(root, text='_____MASS & INERTIA_____').grid(row=17, column=0)
        tk.Label(root, text='Base').grid(row=17, column=1)
        tk.Label(root, text='Mod').grid(row=17, column=2)
        tk.Label(root, text='Base').grid(row=17, column=5)
        tk.Label(root, text='Mod').grid(row=17, column=6)

        tk.Label(root, text="FL Corner Total Mass:").grid(row=18,column=0)
        eFLCornerMass = tk.Entry(root, width=7)
        eFLCornerMass.grid(row=18, column=1)
        eFLCornerMass.insert(0, "678")
        eFLCornerMassMod = tk.Entry(root, width=7)
        eFLCornerMassMod.grid(row=18, column=2)
        eFLCornerMassMod.insert(0, "678")
        tk.Label(root, text=" lbs").grid(row=18,column=3)

        tk.Label(root, text="FL Corner Unsprung Mass:").grid(row=19,column=0)
        eFLCornerUMass = tk.Entry(root, width=7)
        eFLCornerUMass.grid(row=19, column=1)
        eFLCornerUMass.insert(0, "100")
        eFLCornerUMassMod = tk.Entry(root, width=7)
        eFLCornerUMassMod.grid(row=19, column=2)
        eFLCornerUMassMod.insert(0, "100")
        tk.Label(root, text=" lbs").grid(row=19,column=3)

        tk.Label(root, text="FR Corner Total Mass:").grid(row=18,column=7)
        eFRCornerMass = tk.Entry(root, width=7)
        eFRCornerMass.grid(row=18, column=5)
        eFRCornerMass.insert(0, "657")
        eFRCornerMassMod = tk.Entry(root, width=7)
        eFRCornerMassMod.grid(row=18, column=6)
        eFRCornerMassMod.insert(0, "657")

        tk.Label(root, text="FR Corner Unsprung Mass:").grid(row=19,column=7)
        eFRCornerUMass = tk.Entry(root, width=7)
        eFRCornerUMass.grid(row=19, column=5)
        eFRCornerUMass.insert(0, "100")
        eFRCornerUMassMod = tk.Entry(root, width=7)
        eFRCornerUMassMod.grid(row=19, column=6)
        eFRCornerUMassMod.insert(0, "100")

        tk.Label(root, text="RL Corner Total Mass:").grid(row=20,column=0)
        eRLCornerMass = tk.Entry(root, width=7)
        eRLCornerMass.grid(row=20, column=1)
        eRLCornerMass.insert(0, "568")
        eRLCornerMassMod = tk.Entry(root, width=7)
        eRLCornerMassMod.grid(row=20, column=2)
        eRLCornerMassMod.insert(0, "568")
        tk.Label(root, text=" lbs").grid(row=20,column=3)

        tk.Label(root, text="RL Corner Unsprung Mass:").grid(row=21,column=0)
        eRLCornerUMass = tk.Entry(root, width=7)
        eRLCornerUMass.grid(row=21, column=1)
        eRLCornerUMass.insert(0, "120")
        eRLCornerUMassMod = tk.Entry(root, width=7)
        eRLCornerUMassMod.grid(row=21, column=2)
        eRLCornerUMassMod.insert(0, "120")
        tk.Label(root, text=" lbs").grid(row=21,column=3)

        tk.Label(root, text="RR Corner Total Mass:").grid(row=20,column=7)
        eRRCornerMass = tk.Entry(root, width=7)
        eRRCornerMass.grid(row=20, column=5)
        eRRCornerMass.insert(0, "559")
        eRRCornerMassMod = tk.Entry(root, width=7)
        eRRCornerMassMod.grid(row=20, column=6)
        eRRCornerMassMod.insert(0, "559")

        tk.Label(root, text="RR Corner Unsprung Mass:").grid(row=21,column=7)
        eRRCornerUMass = tk.Entry(root, width=7)
        eRRCornerUMass.grid(row=21, column=5)
        eRRCornerUMass.insert(0, "120")
        eRRCornerUMassMod = tk.Entry(root, width=7)
        eRRCornerUMassMod.grid(row=21, column=6)
        eRRCornerUMassMod.insert(0, "120")

        tk.Label(root, text=" CM Height: ").grid(row=22,column=0)
        eCMHeight = tk.Entry(root, width=7)
        eCMHeight.grid(row=22, column=1)
        eCMHeight.insert(0, "19.5")
        eCMHeightMod = tk.Entry(root, width=7)
        eCMHeightMod.grid(row=22, column=2)
        eCMHeightMod.insert(0, "19.5")
        tk.Label(root, text=" in.").grid(row=22,column=3)

        tk.Label(root, text=" Roll Inertia: ").grid(row=23,column=0)
        eRollInertia = tk.Entry(root, width=7)
        eRollInertia.grid(row=23, column=1)
        eRollInertia.insert(0, "1318000")
        eRollInertiaMod = tk.Entry(root, width=7)
        eRollInertiaMod.grid(row=23, column=2)
        eRollInertiaMod.insert(0, "1318000")
        tk.Label(root, text=" lbs*in^2").grid(row=23,column=3)

        #REAR DATA GATHERING #VARIABLE NAMES NEED CHANGING__________________________________________________________________________________________________

        tk.Label(root, text='_______REAR_______').grid(row=0, column=7)
        tk.Label(root, text='Base').grid(row=30, column=1)
        tk.Label(root, text='Mod').grid(row=30, column=2)
        tk.Label(root, text='     ').grid(row=29, column=0)

        tk.Label(root, text="Spring Rate:").grid(row=1,column=7)
        eRSpringRate = tk.Entry(root, width=7)
        eRSpringRate.grid(row=1, column=5)
        eRSpringRate.insert(0, "750")
        eRSpringRateMod = tk.Entry(root, width=7)
        eRSpringRateMod.grid(row=1, column=6)
        eRSpringRateMod.insert(0, "750")

        tk.Label(root, text="Wheel:Spring Motion Ratio:").grid(row=2,column=7)
        eRMotionRatioWS = tk.Entry(root, width=7)
        eRMotionRatioWS.grid(row=2, column=5)
        eRMotionRatioWS.insert(0, "1.48")
        eRMotionRatioWSMod = tk.Entry(root, width=7)
        eRMotionRatioWSMod.grid(row=2, column=6)
        eRMotionRatioWSMod.insert(0, "1.48")

        tk.Label(root, text="Wheel:Damper Motion Ratio:").grid(row=3,column=7)
        eRMotionRatioWD = tk.Entry(root, width=7)
        eRMotionRatioWD.grid(row=3, column=5)
        eRMotionRatioWD.insert(0, "1.05")
        eRMotionRatioWDMod = tk.Entry(root, width=7)
        eRMotionRatioWDMod.grid(row=3, column=6)
        eRMotionRatioWDMod.insert(0, "1.05")

        tk.Label(root, text="Damper Rate, Slow Bump:").grid(row=4,column=7)
        eRDamperRateSB = tk.Entry(root, width=7)
        eRDamperRateSB.grid(row=4, column=5)
        eRDamperRateSB.insert(0, "2384.0")
        eRDamperRateSBMod = tk.Entry(root, width=7)
        eRDamperRateSBMod.grid(row=4, column=6)
        eRDamperRateSBMod.insert(0, "2384.0")

        tk.Label(root, text="Damper Rate, Fast Bump:").grid(row=5,column=7)
        eRDamperRateFB = tk.Entry(root, width=7)
        eRDamperRateFB.grid(row=5, column=5)
        eRDamperRateFB.insert(0, "700")
        eRDamperRateFBMod = tk.Entry(root, width=7)
        eRDamperRateFBMod.grid(row=5, column=6)
        eRDamperRateFBMod.insert(0, "700")

        tk.Label(root, text="Damper Rate, Slow Rebound:").grid(row=6,column=7)
        eRDamperRateSR = tk.Entry(root, width=7)
        eRDamperRateSR.grid(row=6, column=5)
        eRDamperRateSR.insert(0, "4615.4")
        eRDamperRateSRMod = tk.Entry(root, width=7)
        eRDamperRateSRMod.grid(row=6, column=6)
        eRDamperRateSRMod.insert(0, "4615.4")

        tk.Label(root, text="Damper Rate, Fast Rebound:").grid(row=7,column=7)
        eRDamperRateFR = tk.Entry(root, width=7)
        eRDamperRateFR.grid(row=7, column=5)
        eRDamperRateFR.insert(0, "2302.5")
        eRDamperRateFRMod = tk.Entry(root, width=7)
        eRDamperRateFRMod.grid(row=7, column=6)
        eRDamperRateFRMod.insert(0, "2302.5")

        tk.Label(root, text="Knee Speed, Bump:").grid(row=8,column=7)
        eRKneeSpeedBump = tk.Entry(root, width=7)
        eRKneeSpeedBump.grid(row=8, column=5)
        eRKneeSpeedBump.insert(0, "0.130")
        eRKneeSpeedBumpMod = tk.Entry(root, width=7)
        eRKneeSpeedBumpMod.grid(row=8, column=6)
        eRKneeSpeedBumpMod.insert(0, "0.130")

        tk.Label(root, text="Knee Speed, Rebound:").grid(row=9,column=7)
        eRKneeSpeedR = tk.Entry(root, width=7)
        eRKneeSpeedR.grid(row=9, column=5)
        eRKneeSpeedR.insert(0, "0.130")
        eRKneeSpeedRMod = tk.Entry(root, width=7)
        eRKneeSpeedRMod.grid(row=9, column=6)
        eRKneeSpeedRMod.insert(0, "0.130")

        tk.Label(root, text="ARB Rate at Wheel:").grid(row=10,column=7)
        eARBRateR = tk.Entry(root, width=7)
        eARBRateR.grid(row=10, column=5)
        eARBRateR.insert(0, "25")
        eARBRateRMod = tk.Entry(root, width=7)
        eARBRateRMod.grid(row=10, column=6)
        eARBRateRMod.insert(0, "25")

        tk.Label(root, text="Roll Center Height:").grid(row=11,column=7)
        eRCHeightR = tk.Entry(root, width=7)
        eRCHeightR.grid(row=11, column=5)
        eRCHeightR.insert(0, "5.0")
        eRCHeightRMod = tk.Entry(root, width=7)
        eRCHeightRMod.grid(row=11, column=6)
        eRCHeightRMod.insert(0, "5.0")

        tk.Label(root, text="Tire Stiffness:").grid(row=12,column=7)
        eTireKR = tk.Entry(root, width=7)
        eTireKR.grid(row=12, column=5)
        eTireKR.insert(0, "1720")
        eTireKRMod = tk.Entry(root, width=7)
        eTireKRMod.grid(row=12, column=6)
        eTireKRMod.insert(0, "1720")
        
        tk.Label(root, text="Tire Diameter:").grid(row=13,column=7)
        eTireDR = tk.Entry(root, width=7)
        eTireDR.grid(row=13, column=5)
        eTireDR.insert(0, "23.5")
        eTireDRMod = tk.Entry(root, width=7)
        eTireDRMod.grid(row=13, column=6)
        eTireDRMod.insert(0, "23.5")

        tk.Label(root, text="Track Width:").grid(row=14,column=7)
        eRTW = tk.Entry(root, width=7)
        eRTW.grid(row=14, column=5)
        eRTW.insert(0, "62.0")
        eRTWMod = tk.Entry(root, width=7)
        eRTWMod.grid(row=14, column=6)
        eRTWMod.insert(0, "62.0")

        tk.Label(root, text="Aerodynamic Load:").grid(row=15,column=7)
        eRAeroLoad = tk.Entry(root, width=7)
        eRAeroLoad.grid(row=15, column=5)
        eRAeroLoad.insert(0, "30")
        eRAeroLoadMod = tk.Entry(root, width=7)
        eRAeroLoadMod.grid(row=15, column=6)
        eRAeroLoadMod.insert(0, "30")

        #INPUT G FORCE___________________________________________________________________________________________________________

        tk.Label(root, text='___FORCE FUNCTION___').grid(row=30, column=0)

        tk.Label(root, text="Duration:").grid(row=51,column=0)
        eSec = tk.Entry(root, width=7)
        eSec.grid(row=51, column=1)
        eSec.insert(0, "0.8")
        tk.Label(root, text=" s ").grid(row=51,column=3)
        
        tk.Label(root, text="Max Sustained Lateral G:").grid(row=52,column=0)
        eMaxG = tk.Entry(root, width=7)
        eMaxG.grid(row=52, column=1)
        eMaxG.insert(0, "1.4")
        eMaxGMod = tk.Entry(root, width=7)
        eMaxGMod.grid(row=52, column=2)
        eMaxGMod.insert(0, "1.4")
        tk.Label(root, text=" 9.8(m/(s^2)) ").grid(row=52,column=3)
        
        tk.Label(root, text="Ramp Time:").grid(row=53,column=0)
        eRampT = tk.Entry(root, width=7)
        eRampT.grid(row=53, column=1)
        eRampT.insert(0, "0.15")
        eRampTMod = tk.Entry(root, width=7)
        eRampTMod.grid(row=53, column=2)
        eRampTMod.insert(0, "0.15")
        tk.Label(root, text=" s ").grid(row=53,column=3)
        
        tk.Label(root, text="Sin Period:").grid(row=54,column=0)
        eSinT = tk.Entry(root, width=7)
        eSinT.grid(row=54, column=1)
        eSinT.insert(0, "0.7")
        eSinTMod = tk.Entry(root, width=7)
        eSinTMod.grid(row=54, column=2)
        eSinTMod.insert(0, "0.7")
        tk.Label(root, text=" s ").grid(row=54,column=3)

        #Results==========================================================================================================================================
        def RollSimMain():

            BasicParamWindow = tk.Tk()
            BasicParamWindow.title('Basic Suspension Parameters')

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

            SprungWeightDistResult =  RSF_weight_dist(FLSMass, FRSMass, RLSMass, RRSMass, FLSMassMod, FRSMassMod, RLSMassMod, RRSMassMod)
            FSprungWeightDist = SprungWeightDistResult[0]
            FSprungWeightDistMod = SprungWeightDistResult[3]
            TotalSprungMass = SprungWeightDistResult[18]
            TotalSprungMassMod = SprungWeightDistResult[19]

            WeightDistResult =  RSF_weight_dist(FLMass, FRMass, RLMass, RRMass, FLMassMod, FRMassMod, RLMassMod, RRMassMod)

            #FRONT LEFT___________________

            FLWheelRateResult = RSF_wheel_rate(FSpringRate, FMotionRatioWS, FSpringRateMod, FMotionRatioWSMod)
            FLWheelRate = FLWheelRateResult[0]
            FLWheelRateMod = FLWheelRateResult[1]

            FLUndamperRideFrequencyResult = RSF_undamped_ride_freq(FLWheelRate, FLSMass, FLWheelRateMod, FLSMassMod)

            FLDampingRatioSBResult = RSF_corner_damping_ratio(FLWheelRate, FLSMass,  FDamperRateSB, FMotionRatioWD,
                                                    FLWheelRateMod, FLSMassMod,  FDamperRateSBMod, FMotionRatioWDMod)

            FLDampingRatioFBResult = RSF_corner_damping_ratio(FLWheelRate, FLSMass,  FDamperRateFB, FMotionRatioWD,
                                                    FLWheelRateMod, FLSMassMod,  FDamperRateFBMod, FMotionRatioWDMod)

            FLDampingRatioSRResult = RSF_corner_damping_ratio(FLWheelRate, FLSMass,  FDamperRateSR, FMotionRatioWD,
                                                    FLWheelRateMod, FLSMassMod,  FDamperRateSRMod, FMotionRatioWDMod)

            FLDampingRatioFRResult = RSF_corner_damping_ratio(FLWheelRate, FLSMass,  FDamperRateFR, FMotionRatioWD,
                                                    FLWheelRateMod, FLSMassMod,  FDamperRateFRMod, FMotionRatioWDMod)

            #FRONT RIGHT___________________

            FRWheelRateResult = RSF_wheel_rate(FSpringRate,FMotionRatioWS,FSpringRateMod, FMotionRatioWSMod)
            FRWheelRate = FRWheelRateResult[0]
            FRWheelRateMod = FRWheelRateResult[1]

            FRUndamperRideFrequencyResult = RSF_undamped_ride_freq(FRWheelRate, FRSMass, FRWheelRateMod, FRSMassMod)

            FRDampingRatioSBResult = RSF_corner_damping_ratio(FRWheelRate, FRSMass,  FDamperRateSB, FMotionRatioWD,
                                                    FRWheelRateMod, FRSMassMod,  FDamperRateSBMod, FMotionRatioWDMod)

            FRDampingRatioFBResult = RSF_corner_damping_ratio(FRWheelRate, FRSMass,  FDamperRateFB, FMotionRatioWD,
                                                    FRWheelRateMod, FRSMassMod,  FDamperRateFBMod, FMotionRatioWDMod)

            FRDampingRatioSRResult = RSF_corner_damping_ratio(FRWheelRate, FRSMass,  FDamperRateSR, FMotionRatioWD,
                                                    FRWheelRateMod, FRSMassMod,  FDamperRateSRMod, FMotionRatioWDMod)

            FRDampingRatioFRResult = RSF_corner_damping_ratio(FRWheelRate, FRSMass,  FDamperRateFR, FMotionRatioWD,
                                                    FRWheelRateMod, FRSMassMod,  FDamperRateFRMod, FMotionRatioWDMod)

            #REAR LEFT___________________

            RLWheelRateResult = RSF_wheel_rate(RSpringRate, RMotionRatioWS, RSpringRateMod, RMotionRatioWSMod)
            RLWheelRate = RLWheelRateResult[0]
            RLWheelRateMod = RLWheelRateResult[1]

            RLUndamperRideFrequencyResult = RSF_undamped_ride_freq(RLWheelRate, RLSMass, RLWheelRateMod, RLSMassMod)

            RLDampingRatioSBResult = RSF_corner_damping_ratio(RLWheelRate, RLSMass,  RDamperRateSB, RMotionRatioWD,
                                                    RLWheelRateMod, RLSMassMod,  RDamperRateSBMod, RMotionRatioWDMod)

            RLDampingRatioFBResult = RSF_corner_damping_ratio(RLWheelRate, RLSMass,  RDamperRateFB, RMotionRatioWD,
                                                    RLWheelRateMod, RLSMassMod,  RDamperRateFBMod, RMotionRatioWDMod)

            RLDampingRatioSRResult = RSF_corner_damping_ratio(RLWheelRate, RLSMass,  RDamperRateSR, RMotionRatioWD,
                                                    RLWheelRateMod, RLSMassMod,  RDamperRateSRMod, RMotionRatioWDMod)

            RLDampingRatioFRResult = RSF_corner_damping_ratio(RLWheelRate, RLSMass,  RDamperRateFR, RMotionRatioWD,
                                                    RLWheelRateMod, RLSMassMod,  RDamperRateFRMod, RMotionRatioWDMod)

            #REAR RIGHT___________________

            RRWheelRateResult = RSF_wheel_rate(RSpringRate,RMotionRatioWS,RSpringRateMod, RMotionRatioWSMod)
            RRWheelRate = RRWheelRateResult[0]
            RRWheelRateMod = RRWheelRateResult[1]

            RRUndamperRideFrequencyResult = RSF_undamped_ride_freq(RRWheelRate, RRSMass, RRWheelRateMod, RRSMassMod)

            RRDampingRatioSBResult = RSF_corner_damping_ratio(RRWheelRate, RRSMass,  RDamperRateSB, RMotionRatioWD,
                                                    RRWheelRateMod, RRSMassMod,  RDamperRateSBMod, RMotionRatioWDMod)

            RRDampingRatioFBResult = RSF_corner_damping_ratio(RRWheelRate, RRSMass,  RDamperRateFB, RMotionRatioWD,
                                                    RRWheelRateMod, RRSMassMod,  RDamperRateFBMod, RMotionRatioWDMod)

            RRDampingRatioSRResult = RSF_corner_damping_ratio(RRWheelRate, RRSMass,  RDamperRateSR, RMotionRatioWD,
                                                    RRWheelRateMod, RRSMassMod,  RDamperRateSRMod, RMotionRatioWDMod)

            RRDampingRatioFRResult = RSF_corner_damping_ratio(RRWheelRate, RRSMass,  RDamperRateFR, RMotionRatioWD,
                                                    RRWheelRateMod, RRSMassMod,  RDamperRateFRMod, RMotionRatioWDMod)

            #Steady State Roll Outputs
            ssro = RSF_steady_state(
                FSprungWeightDist, CMHeight, FRCHeight, RRCHeight,
                FRWheelRate, RRWheelRate, TotalSprungMass, FLUMass+FRUMass, RLUMass+RRUMass, Gforce, TWf, TWr,
                ARBRateF, ARBRateR, FMotionRatioWS, RMotionRatioWS, FMotionRatioWD, RMotionRatioWD,
                FAeroLoad, RAeroLoad, RollInertia,
                (FDamperRateSB/(FMotionRatioWD**2)), (FDamperRateSR/(FMotionRatioWD**2)), (RDamperRateSB/(RMotionRatioWD**2)), (RDamperRateSR/(RMotionRatioWD**2)),
                (FDamperRateFB/(FMotionRatioWD**2)), (FDamperRateFR/(FMotionRatioWD**2)), (RDamperRateFB/(RMotionRatioWD**2)), (RDamperRateFR/(RMotionRatioWD**2)),
                TireDF, TireDR, TireKF, TireKR 
            )

            ssro_mod = RSF_steady_state(
                FSprungWeightDistMod, CMHeightMod, FRCHeightMod, RRCHeightMod,
                FRWheelRateMod, RRWheelRateMod, TotalSprungMassMod, FLUMassMod+FRUMassMod, RLUMassMod+RRUMassMod, GforceMod, TWfMod, TWrMod,
                ARBRateFMod, ARBRateRMod, FMotionRatioWSMod, RMotionRatioWSMod, FMotionRatioWDMod, RMotionRatioWDMod,
                FAeroLoadMod, RAeroLoadMod, RollInertiaMod,
                (FDamperRateSBMod/(FMotionRatioWDMod**2)), (FDamperRateSRMod/(FMotionRatioWDMod**2)), (RDamperRateSBMod/(RMotionRatioWDMod**2)), (RDamperRateSRMod/(RMotionRatioWDMod**2)),
                (FDamperRateFBMod/(FMotionRatioWDMod**2)), (FDamperRateFRMod/(FMotionRatioWDMod**2)), (RDamperRateFBMod/(RMotionRatioWDMod**2)), (RDamperRateFRMod/(RMotionRatioWDMod**2)),
                TireDFMod, TireDRMod, TireKFMod, TireKRMod
            )

            #Display Results
            tk.Label(BasicParamWindow, text='_____STEADY STATE CORNERING_____').grid(row=71, column=0)
            tk.Label(BasicParamWindow, text='(Base/ Mod/ %)').grid(row=71, column=1)

            tk.Label(BasicParamWindow, text = ' Front Weight Transfer: ').grid(row=72, column=0)
            tk.Label(BasicParamWindow, text = ssro[1] + '/ ' + ssro_mod[1] + '/ ' + str(round(100*(ssro_mod[9]-ssro[9])/ssro[9], 1))).grid(row=72, column=1)
            tk.Label(BasicParamWindow, text = '%').grid(row=72, column=2)
            tk.Label(BasicParamWindow, text = ' Rear Weight Transfer: ').grid(row=73, column=0)
            tk.Label(BasicParamWindow, text = ssro[2] + '/ ' + ssro_mod[2] + '/ ' + str(round(100*(ssro_mod[10]-ssro[10])/ssro[10], 1))).grid(row=73, column=1)
            tk.Label(BasicParamWindow, text = '%').grid(row=73, column=2)
            tk.Label(BasicParamWindow, text = ' F/R Lateral Load Transfer Ratio: ').grid(row=74, column=0)
            tk.Label(BasicParamWindow, text = ssro[3] + '/ ' + ssro_mod[3] + '/ ' + str(round(100*(ssro_mod[11]-ssro[11])/ssro[11], 1))).grid(row=74, column=1)
            tk.Label(BasicParamWindow, text = '-/-').grid(row=74, column=2)

            tk.Label(BasicParamWindow, text='     ').grid(row=75, column=0)

            tk.Label(BasicParamWindow, text = ' Natural Roll Frequency: ').grid(row=76, column=0)
            tk.Label(BasicParamWindow, text = ssro[17] + '/ ' + ssro_mod[17] + '/ ' + str(round(100*(ssro_mod[16]-ssro[16])/ssro[16], 1))).grid(row=76, column=1)
            tk.Label(BasicParamWindow, text = 'hz').grid(row=76, column=2)
            tk.Label(BasicParamWindow, text = ' Roll Damping Ratio (Slow): ').grid(row=77, column=0)
            tk.Label(BasicParamWindow, text = ssro[19] + '/ ' + ssro_mod[19] + '/ ' + str(round(100*(ssro_mod[18]-ssro[18])/ssro[18], 1))).grid(row=77, column=1)
            tk.Label(BasicParamWindow, text = 'hz').grid(row=77, column=2)
            tk.Label(BasicParamWindow, text = ' Roll Damping Ratio (Fast): ').grid(row=78, column=0)
            tk.Label(BasicParamWindow, text = ssro[21] + '/ ' + ssro_mod[21] + '/ ' + str(round(100*(ssro_mod[20]-ssro[20])/ssro[20], 1))).grid(row=78, column=1)
            tk.Label(BasicParamWindow, text = 'hz').grid(row=78, column=2)
            tk.Label(BasicParamWindow, text = ' Damped Roll Frequency (Slow): ').grid(row=79, column=0)
            tk.Label(BasicParamWindow, text = ssro[23] + '/ ' + ssro_mod[23] + '/ ' + str(round(100*(ssro_mod[22]-ssro[22])/ssro[22], 1))).grid(row=79, column=1)
            tk.Label(BasicParamWindow, text = 'hz').grid(row=79, column=2)
            tk.Label(BasicParamWindow, text = ' Damped Roll Frequency (Fast): ').grid(row=80, column=0)
            tk.Label(BasicParamWindow, text = ssro[25] + '/ ' + ssro_mod[25] + '/ ' + str(round(100*(ssro_mod[24]-ssro[24])/ssro[24], 1))).grid(row=80, column=1)
            tk.Label(BasicParamWindow, text = 'hz').grid(row=80, column=2)

            tk.Label(BasicParamWindow, text='     ').grid(row=81, column=0)

            tk.Label(BasicParamWindow, text = ' Roll Angle (About Roll Axis): ').grid(row=82, column=0)
            tk.Label(BasicParamWindow, text = ssro[0] + '/ ' + ssro_mod[0] + '/ ' + str(round(100*(ssro_mod[8]-ssro[8])/ssro[8], 1))).grid(row=82, column=1)
            tk.Label(BasicParamWindow, text = 'deg').grid(row=82, column=2)
            tk.Label(BasicParamWindow, text = ' Front Spring Defl. from Rest: ').grid(row=83, column=0)
            tk.Label(BasicParamWindow, text = ssro[4] + '/ ' + ssro_mod[4] + '/ ' + str(round(100*(ssro_mod[12]-ssro[12])/ssro[12], 1))).grid(row=83, column=1)
            tk.Label(BasicParamWindow, text = 'in.').grid(row=83, column=2)
            tk.Label(BasicParamWindow, text = ' Front Damper Defl. from Rest: ').grid(row=84, column=0)
            tk.Label(BasicParamWindow, text = ssro[6] + '/ ' + ssro_mod[6] + '/ ' + str(round(100*(ssro_mod[14]-ssro[14])/ssro[14], 1))).grid(row=84, column=1)
            tk.Label(BasicParamWindow, text = 'in.').grid(row=84, column=2)
            tk.Label(BasicParamWindow, text = ' Rear Spring Defl. from Rest: ').grid(row=85, column=0)
            tk.Label(BasicParamWindow, text = ssro[5] + '/ ' + ssro_mod[5] + '/ ' + str(round(100*(ssro_mod[13]-ssro[13])/ssro[13], 1))).grid(row=85, column=1)
            tk.Label(BasicParamWindow, text = 'in.').grid(row=85, column=2)
            tk.Label(BasicParamWindow, text = ' Rear Damper Defl. from Rest: ').grid(row=86, column=0)
            tk.Label(BasicParamWindow, text = ssro[7] + '/ ' + ssro_mod[7] + '/ ' + str(round(100*(ssro_mod[15]-ssro[15])/ssro[15], 1))).grid(row=86, column=1)
            tk.Label(BasicParamWindow, text = 'in.').grid(row=86, column=2)

            tk.Label(BasicParamWindow, text='     ').grid(row=99, column=0)

            tk.Label(BasicParamWindow, text='_______FL CORNER_______').grid(row=100, column=0)
            tk.Label(BasicParamWindow, text='(Base/ Mod/ %)').grid(row=100, column=1)
            tk.Label(BasicParamWindow, text='_______FR CORNER_______').grid(row=100, column=5)
            tk.Label(BasicParamWindow, text='(Base/ Mod/ %)').grid(row=100, column=6)

            tk.Label(BasicParamWindow, text = ' Wheel Rate: ').grid(row=101, column=0)
            tk.Label(BasicParamWindow, text = FLWheelRateResult[3] + '/ ' + FLWheelRateResult[4] + '/ ' + FLWheelRateResult[5]).grid(row=101, column=1)
            tk.Label(BasicParamWindow, text = 'lbs/in.').grid(row=101, column=2)

            tk.Label(BasicParamWindow, text = ' Undamped Ride Frequency: ').grid(row=102, column=0)
            tk.Label(BasicParamWindow, text = FLUndamperRideFrequencyResult[3] + '/ ' + FLUndamperRideFrequencyResult[4] + '/ ' + FLUndamperRideFrequencyResult[5]).grid(row=102, column=1)
            tk.Label(BasicParamWindow, text = 'hz').grid(row=102, column=2)

            tk.Label(BasicParamWindow, text = ' Damping Ratio, Slow Bump: ').grid(row=103, column=0)
            tk.Label(BasicParamWindow, text = FLDampingRatioSBResult[3] + '/ ' + FLDampingRatioSBResult[4] + '/ ' + FLDampingRatioSBResult[5]).grid(row=103, column=1)
            tk.Label(BasicParamWindow, text = '-/-').grid(row=103, column=2)

            tk.Label(BasicParamWindow, text = ' Damping Ratio, Fast Bump: ').grid(row=104, column=0)
            tk.Label(BasicParamWindow, text = FLDampingRatioFBResult[3] + '/ ' + FLDampingRatioFBResult[4] + '/ ' + FLDampingRatioFBResult[5]).grid(row=104, column=1)
            tk.Label(BasicParamWindow, text = '-/-').grid(row=104, column=2)

            tk.Label(BasicParamWindow, text = ' Damping Ratio, Slow Rebound: ').grid(row=105, column=0)
            tk.Label(BasicParamWindow, text = FLDampingRatioSRResult[3] + '/ ' + FLDampingRatioSRResult[4] + '/ ' + FLDampingRatioSRResult[5]).grid(row=105, column=1)
            tk.Label(BasicParamWindow, text = '-/-').grid(row=105, column=2)

            tk.Label(BasicParamWindow, text = ' Damping Ratio, Fast Rebound: ').grid(row=106, column=0)
            tk.Label(BasicParamWindow, text = FLDampingRatioFRResult[3] + '/ ' + FLDampingRatioFRResult[4] + '/ ' + FLDampingRatioFRResult[5]).grid(row=106, column=1)
            tk.Label(BasicParamWindow, text = '-/-').grid(row=106, column=2)

            tk.Label(BasicParamWindow, text = ' Wheel Rate: ').grid(row=101, column=5)
            tk.Label(BasicParamWindow, text = FRWheelRateResult[3] + '/ ' + FRWheelRateResult[4] + '/ ' + FRWheelRateResult[5]).grid(row=101, column=6)
            tk.Label(BasicParamWindow, text = 'lbs/in.').grid(row=101, column=7)

            tk.Label(BasicParamWindow, text = ' Undamped Ride Frequency: ').grid(row=102, column=5)
            tk.Label(BasicParamWindow, text = FRUndamperRideFrequencyResult[3] + '/ ' + FRUndamperRideFrequencyResult[4] + '/ ' + FRUndamperRideFrequencyResult[5]).grid(row=102, column=6)
            tk.Label(BasicParamWindow, text = 'hz').grid(row=102, column=7)

            tk.Label(BasicParamWindow, text = ' Damping Ratio, Slow Bump: ').grid(row=103, column=5)
            tk.Label(BasicParamWindow, text = FRDampingRatioSBResult[3] + '/ ' + FRDampingRatioSBResult[4] + '/ ' + FRDampingRatioSBResult[5]).grid(row=103, column=6)
            tk.Label(BasicParamWindow, text = '-/-').grid(row=103, column=7)

            tk.Label(BasicParamWindow, text = ' Damping Ratio, Fast Bump: ').grid(row=104, column=5)
            tk.Label(BasicParamWindow, text = FRDampingRatioFBResult[3] + '/ ' + FRDampingRatioFBResult[4] + '/ ' + FRDampingRatioFBResult[5]).grid(row=104, column=6)
            tk.Label(BasicParamWindow, text = '-/-').grid(row=104, column=7)

            tk.Label(BasicParamWindow, text = ' Damping Ratio, Slow Rebound: ').grid(row=105, column=5)
            tk.Label(BasicParamWindow, text = FRDampingRatioSRResult[3] + '/ ' + FRDampingRatioSRResult[4] + '/ ' + FRDampingRatioSRResult[5]).grid(row=105, column=6)
            tk.Label(BasicParamWindow, text = '-/-').grid(row=105, column=7)

            tk.Label(BasicParamWindow, text = ' Damping Ratio, Fast Rebound: ').grid(row=106, column=5)
            tk.Label(BasicParamWindow, text = FRDampingRatioFRResult[3] + '/ ' + FRDampingRatioFRResult[4] + '/ ' + FRDampingRatioFRResult[5]).grid(row=106, column=6)
            tk.Label(BasicParamWindow, text = '-/-').grid(row=106, column=7)

            tk.Label(BasicParamWindow, text='     ').grid(row=119, column=0)

            tk.Label(BasicParamWindow, text='_______RL CORNER_______').grid(row=120, column=0)
            tk.Label(BasicParamWindow, text='(Base/ Mod/ %)').grid(row=120, column=1)
            tk.Label(BasicParamWindow, text='_______RR CORNER_______').grid(row=120, column=5)
            tk.Label(BasicParamWindow, text='(Base/ Mod/ %)').grid(row=120, column=6)

            tk.Label(BasicParamWindow, text = ' Wheel Rate: ').grid(row=121, column=0)
            tk.Label(BasicParamWindow, text = RLWheelRateResult[3] + '/ ' + RLWheelRateResult[4] + '/ ' + RLWheelRateResult[5]).grid(row=121, column=1)
            tk.Label(BasicParamWindow, text = 'lbs/in.').grid(row=121, column=2)

            tk.Label(BasicParamWindow, text = ' Undamped Ride Frequency: ').grid(row=122, column=0)
            tk.Label(BasicParamWindow, text = RLUndamperRideFrequencyResult[3] + '/ ' + RLUndamperRideFrequencyResult[4] + '/ ' + RLUndamperRideFrequencyResult[5]).grid(row=122, column=1)
            tk.Label(BasicParamWindow, text = 'hz').grid(row=122, column=2)

            tk.Label(BasicParamWindow, text = ' Damping Ratio, Slow Bump: ').grid(row=123, column=0)
            tk.Label(BasicParamWindow, text = RLDampingRatioSBResult[3] + '/ ' + RLDampingRatioSBResult[4] + '/ ' + RLDampingRatioSBResult[5]).grid(row=123, column=1)
            tk.Label(BasicParamWindow, text = '-/-').grid(row=123, column=2)

            tk.Label(BasicParamWindow, text = ' Damping Ratio, Fast Bump: ').grid(row=124, column=0)
            tk.Label(BasicParamWindow, text = RLDampingRatioFBResult[3] + '/ ' + RLDampingRatioFBResult[4] + '/ ' + RLDampingRatioFBResult[5]).grid(row=124, column=1)
            tk.Label(BasicParamWindow, text = '-/-').grid(row=124, column=2)

            tk.Label(BasicParamWindow, text = ' Damping Ratio, Slow Rebound: ').grid(row=125, column=0)
            tk.Label(BasicParamWindow, text = RLDampingRatioSRResult[3] + '/ ' + RLDampingRatioSRResult[4] + '/ ' + RLDampingRatioSRResult[5]).grid(row=125, column=1)
            tk.Label(BasicParamWindow, text = '-/-').grid(row=125, column=2)

            tk.Label(BasicParamWindow, text = ' Damping Ratio, Fast Rebound: ').grid(row=126, column=0)
            tk.Label(BasicParamWindow, text = RLDampingRatioFRResult[3] + '/ ' + RLDampingRatioFRResult[4] + '/ ' + RLDampingRatioFRResult[5]).grid(row=126, column=1)
            tk.Label(BasicParamWindow, text = '-/-').grid(row=126, column=2)

            tk.Label(BasicParamWindow, text = ' Wheel Rate: ').grid(row=121, column=5)
            tk.Label(BasicParamWindow, text = RRWheelRateResult[3] + '/ ' + RRWheelRateResult[4] + '/ ' + RRWheelRateResult[5]).grid(row=121, column=6)
            tk.Label(BasicParamWindow, text = 'lbs/in.').grid(row=121, column=7)

            tk.Label(BasicParamWindow, text = ' Undamped Ride Frequency: ').grid(row=122, column=5)
            tk.Label(BasicParamWindow, text = RRUndamperRideFrequencyResult[3] + '/ ' + RRUndamperRideFrequencyResult[4] + '/ ' + RRUndamperRideFrequencyResult[5]).grid(row=122, column=6)
            tk.Label(BasicParamWindow, text = 'hz').grid(row=122, column=7)

            tk.Label(BasicParamWindow, text = ' Damping Ratio, Slow Bump: ').grid(row=123, column=5)
            tk.Label(BasicParamWindow, text = RRDampingRatioSBResult[3] + '/ ' + RRDampingRatioSBResult[4] + '/ ' + RRDampingRatioSBResult[5]).grid(row=123, column=6)
            tk.Label(BasicParamWindow, text = '-/-').grid(row=123, column=7)

            tk.Label(BasicParamWindow, text = ' Damping Ratio, Fast Bump: ').grid(row=124, column=5)
            tk.Label(BasicParamWindow, text = RRDampingRatioFBResult[3] + '/ ' + RRDampingRatioFBResult[4] + '/ ' + RRDampingRatioFBResult[5]).grid(row=124, column=6)
            tk.Label(BasicParamWindow, text = '-/-').grid(row=124, column=7)

            tk.Label(BasicParamWindow, text = ' Damping Ratio, Slow Rebound: ').grid(row=125, column=5)
            tk.Label(BasicParamWindow, text = RRDampingRatioSRResult[3] + '/ ' + RRDampingRatioSRResult[4] + '/ ' + RRDampingRatioSRResult[5]).grid(row=125, column=6)
            tk.Label(BasicParamWindow, text = '-/-').grid(row=125, column=7)

            tk.Label(BasicParamWindow, text = ' Damping Ratio, Fast Rebound: ').grid(row=126, column=5)
            tk.Label(BasicParamWindow, text = RRDampingRatioFRResult[3] + '/ ' + RRDampingRatioFRResult[4] + '/ ' + RRDampingRatioFRResult[5]).grid(row=126, column=6)
            tk.Label(BasicParamWindow, text = '-/-').grid(row=126, column=7)

            tk.Label(BasicParamWindow, text='     ').grid(row=139, column=0)
            tk.Label(BasicParamWindow, text='_______WEIGHT DIST._______').grid(row=140, column=0)
            tk.Label(BasicParamWindow, text='(Base/ Mod/ %)').grid(row=140, column=1)

            tk.Label(BasicParamWindow, text = ' Front Weight: ').grid(row=141, column=0)
            tk.Label(BasicParamWindow, text = WeightDistResult[9] + '/ ' + WeightDistResult[12] + '/ ' + WeightDistResult[15]).grid(row=141, column=1)
            tk.Label(BasicParamWindow, text = '%').grid(row=141, column=2)

            tk.Label(BasicParamWindow, text = ' Left Weight: ').grid(row=142, column=0)
            tk.Label(BasicParamWindow, text = WeightDistResult[10] + '/ ' + WeightDistResult[13] + '/ ' + WeightDistResult[16]).grid(row=142, column=1)
            tk.Label(BasicParamWindow, text = '%').grid(row=142, column=2)

            tk.Label(BasicParamWindow, text = ' FL+RR Cross-Weight: ').grid(row=143, column=0)
            tk.Label(BasicParamWindow, text = WeightDistResult[11] + '/ ' + WeightDistResult[14] + '/ ' + WeightDistResult[17]).grid(row=143, column=1)
            tk.Label(BasicParamWindow, text = '%').grid(row=143, column=2)

            BasicParamWindow.mainloop()

        #DAMPER PLOTS==========================================================================================================
        def DamperPlots():

            DamperWindow = tk.Tk()
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

            x=[0.3, FKneeSpeedR, 0, FKneeSpeedBump, 0.3]
            y=[-FKneeSpeedR*FDamperRateSR-(0.3-FKneeSpeedR)*FDamperRateFR,
            -FKneeSpeedR*FDamperRateSR,
            0,
            FKneeSpeedBump*FDamperRateSB,
            FKneeSpeedBump*FDamperRateSB+(0.3-FKneeSpeedBump)*FDamperRateFB]

            x_mod=[0.3, FKneeSpeedRMod, 0, FKneeSpeedBumpMod, 0.3]
            y_mod=[-FKneeSpeedRMod*FDamperRateSRMod-(0.3-FKneeSpeedRMod)*FDamperRateFRMod,
                -FKneeSpeedRMod*FDamperRateSRMod,
                0,
                FKneeSpeedBumpMod*FDamperRateSBMod,
                FKneeSpeedBumpMod*FDamperRateSBMod+(0.3-FKneeSpeedBumpMod)*FDamperRateFBMod]

            rx=[0.3, RKneeSpeedR, 0, RKneeSpeedBump, 0.3]
            ry=[-RKneeSpeedR*RDamperRateSR-(0.3-RKneeSpeedR)*RDamperRateFR,
                -RKneeSpeedR*RDamperRateSR,
                0,
                RKneeSpeedBump*RDamperRateSB,
                RKneeSpeedBump*RDamperRateSB+(0.3-RKneeSpeedBump)*RDamperRateFB]

            rx_mod=[0.3, RKneeSpeedRMod, 0, RKneeSpeedBumpMod, 0.3]
            ry_mod=[-RKneeSpeedRMod*RDamperRateSRMod-(0.3-RKneeSpeedRMod)*RDamperRateFRMod,
                -RKneeSpeedRMod*RDamperRateSRMod,
                0,
                RKneeSpeedBumpMod*RDamperRateSBMod,
                RKneeSpeedBumpMod*RDamperRateSBMod+(0.3-RKneeSpeedBumpMod)*RDamperRateFBMod]

            fig, (ax1, ax2) = plt.subplots(2, figsize=(7,8))
            fig.suptitle('Damper Plot (N v. m/s), Base and Mod')

            ax1.plot(x, y, label='Base')
            ax1.plot(x_mod, y_mod, label='Mod')
            ax1.set_ylabel('N, Front')
            ax1.grid()
            ax1.legend()

            ax2.plot(rx, ry, label = 'Base')
            ax2.plot(rx_mod, ry_mod, label = 'Mod')
            ax2.set_ylabel('N, Rear')
            ax2.grid()
            ax2.legend()

            canvas = FigureCanvasTkAgg(fig, master = DamperWindow)   
            canvas.draw() 
            canvas.get_tk_widget().pack()

            DamperWindow.mainloop()

        #TRANSIENT RESPONSE WINDOW________________________________________________________________________________________________
        def Resp3(f_type):

            StepWin = tk.Tk()
            StepWin.title('Transient Lateral G Response (Base, Mod)')
            fig = Figure()

            FSpringRate = float(eFSpringRate.get())
            FSpringRateMod = float(eFSpringRateMod.get())
            RSpringRate = float(eRSpringRate.get())
            RSpringRateMod = float(eRSpringRateMod.get())

            WS_motion_ratio_f = float(eFMotionRatioWS.get())
            WS_motion_ratio_f_mod = float(eFMotionRatioWSMod.get())
            WD_motion_ratio_f = float(eFMotionRatioWD.get())
            WD_motion_ratio_f_mod = float(eFMotionRatioWDMod.get())
            WS_motion_ratio_r = float(eRMotionRatioWS.get())
            WS_motion_ratio_r_mod = float(eRMotionRatioWSMod.get())
            WD_motion_ratio_r = float(eRMotionRatioWD.get())
            WD_motion_ratio_r_mod = float(eRMotionRatioWDMod.get())

            Csb_f = float(eFDamperRateSB.get())
            Csb_f_mod = float(eFDamperRateSBMod.get())
            Cfb_f = float(eFDamperRateFB.get())
            Cfb_f_mod = float(eFDamperRateFBMod.get())
            Csr_f = float(eFDamperRateSR.get())
            Csr_f_mod = float(eFDamperRateSRMod.get())
            Cfr_f = float(eFDamperRateFR.get())
            Cfr_f_mod = float(eFDamperRateFRMod.get())
            Csb_r = float(eRDamperRateSB.get())
            Csb_r_mod = float(eRDamperRateSBMod.get())
            Cfb_r = float(eRDamperRateFB.get())
            Cfb_r_mod = float(eRDamperRateFBMod.get())
            Csr_r = float(eRDamperRateSR.get())
            Csr_r_mod = float(eRDamperRateSRMod.get())
            Cfr_r = float(eRDamperRateFR.get())
            Cfr_r_mod = float(eRDamperRateFRMod.get())

            bypassV_fb = float(eFKneeSpeedBump.get())
            bypassV_fb_mod = float(eFKneeSpeedBumpMod.get())
            bypassV_fr = float(eFKneeSpeedR.get())
            bypassV_fr_mod = float(eFKneeSpeedRMod.get())
            bypassV_rb = float(eRKneeSpeedBump.get())
            bypassV_rb_mod = float(eRKneeSpeedBumpMod.get())
            bypassV_rr = float(eRKneeSpeedR.get())
            bypassV_rr_mod = float(eRKneeSpeedRMod.get())

            #...Corner Masses
            FLMass = float(eFLCornerMass.get())
            FRMass = float(eFRCornerMass.get())
            RLMass = float(eRLCornerMass.get())
            RRMass = float(eRRCornerMass.get())
            flusm = UnitValuePair(float(eFLCornerUMass.get()), 'lbs')
            frusm = UnitValuePair(float(eFRCornerUMass.get()), 'lbs')
            rlusm = UnitValuePair(float(eRLCornerUMass.get()), 'lbs')
            rrusm = UnitValuePair(float(eRRCornerUMass.get()), 'lbs')
            FLMassMod = float(eFLCornerMassMod.get())
            FRMassMod = float(eFRCornerMassMod.get())
            RLMassMod = float(eRLCornerMassMod.get())
            RRMassMod = float(eRRCornerMassMod.get())
            flusm_mod = UnitValuePair(float(eFLCornerUMassMod.get()), 'lbs')
            frusm_mod = UnitValuePair(float(eFRCornerUMassMod.get()), 'lbs')
            rlusm_mod = UnitValuePair(float(eRLCornerUMassMod.get()), 'lbs')
            rrusm_mod = UnitValuePair(float(eRRCornerUMassMod.get()), 'lbs')

            flsm = UnitValuePair(float(FLMass - flusm.value), 'lbs')
            frsm = UnitValuePair(float(FRMass - frusm.value), 'lbs')
            rlsm = UnitValuePair(float(RLMass - rlusm.value), 'lbs')
            rrsm = UnitValuePair(float(RRMass - rrusm.value), 'lbs')
            flsm_mod = UnitValuePair(float(FLMassMod - flusm_mod.value), 'lbs')
            frsm_mod = UnitValuePair(float(FRMassMod - frusm_mod.value), 'lbs')
            rlsm_mod = UnitValuePair(float(RLMassMod - rlusm_mod.value), 'lbs')
            rrsm_mod = UnitValuePair(float(RRMassMod - rrusm_mod.value), 'lbs')

            cg_height = UnitValuePair(float(eCMHeight.get()), 'in')
            cg_height_mod = UnitValuePair(float(eCMHeightMod.get()), 'in')
            rc_height_f = UnitValuePair(float(eRCHeightF.get()), 'in')
            rc_height_f_mod = UnitValuePair(float(eRCHeightFMod.get()), 'in')
            rc_height_r = UnitValuePair(float(eRCHeightR.get()), 'in')
            rc_height_r_mod = UnitValuePair(float(eRCHeightRMod.get()), 'in')
            tw_f = UnitValuePair(float(eFTW.get()), 'in')
            tw_f_mod = UnitValuePair(float(eFTWMod.get()), 'in')
            tw_r = UnitValuePair(float(eRTW.get()), 'in')
            tw_r_mod = UnitValuePair(float(eRTWMod.get()), 'in')
            Gforce = float(eMaxG.get())
            GforceMod = float(eMaxGMod.get())
            
            Karb_f = UnitValuePair(float(eARBRateF.get()), 'lbf/in')
            Karb_f_mod = UnitValuePair(float(eARBRateFMod.get()), 'lbf/in')
            Karb_r = UnitValuePair(float(eARBRateR.get()), 'lbf/in')
            Karb_r_mod = UnitValuePair(float(eARBRateRMod.get()), 'lbf/in')
            aero_load_f = UnitValuePair(float(eFAeroLoad.get()), 'lbf')
            aero_load_f_mod = UnitValuePair(float(eFAeroLoadMod.get()), 'lbf')
            aero_load_r = UnitValuePair(float(eRAeroLoad.get()), 'lbf')
            aero_load_r_mod = UnitValuePair(float(eRAeroLoadMod.get()), 'lbf')
            
            Kt_f = UnitValuePair(float(eTireKF.get()), 'lbf/in')
            Kt_f_mod = UnitValuePair(float(eTireKFMod.get()), 'lbf/in')
            Kt_r = UnitValuePair(float(eTireKR.get()), 'lbf/in')
            Kt_r_mod = UnitValuePair(float(eTireKRMod.get()), 'lbf/in')
            tire_diam_f = UnitValuePair(float(eTireDF.get()), 'in')
            tire_diam_f_mod = UnitValuePair(float(eTireDFMod.get()), 'in')
            tire_diam_r = UnitValuePair(float(eTireDR.get()), 'in')
            tire_diam_r_mod = UnitValuePair(float(eTireDRMod.get()), 'in')

            roll_inertia = UnitValuePair(float(eRollInertia.get()), 'lbs*in^2')
            roll_inertia_mod = UnitValuePair(float(eRollInertiaMod.get()), 'lbs*in^2')
            
            seconds = float(eSec.get())
            rampT = float(eRampT.get())
            rampTMod = float(eRampTMod.get())
            p = float(eSinT.get())
            pMod = float(eSinTMod.get())

            FRWheelRateResult = RSF_wheel_rate(FSpringRate,WS_motion_ratio_f,FSpringRateMod, WS_motion_ratio_f_mod)
            Ks_f = UnitValuePair(float(FRWheelRateResult[0]), 'lbf/in')
            Ks_f_mod = UnitValuePair(float(FRWheelRateResult[1]), 'lbf/in')

            RRWheelRateResult = RSF_wheel_rate(RSpringRate,WS_motion_ratio_r,RSpringRateMod, WS_motion_ratio_r_mod)
            Ks_r = UnitValuePair(float(RRWheelRateResult[0]), 'lbf/in')
            Ks_r_mod = UnitValuePair(float(RRWheelRateResult[1]), 'lbf/in')

            SprungWeightDistResult =  RSF_weight_dist(flsm.value, frsm.value, rlsm.value, rrsm.value, flsm_mod.value, frsm_mod.value, rlsm_mod.value, rrsm_mod.value)
            FSprungWeightDist = SprungWeightDistResult[0]
            FSprungWeightDistMod = SprungWeightDistResult[3]
            TotalSprungMass = SprungWeightDistResult[18]
            TotalSprungMassMod = SprungWeightDistResult[19]

            ssro = RSF_steady_state(
                FSprungWeightDist, cg_height.value, rc_height_f.value, rc_height_r.value,
                Ks_f.value, Ks_r.value, TotalSprungMass, flusm.value+frusm.value, rlusm.value+rrusm.value, Gforce, tw_f.value, tw_r.value,
                Karb_f.value, Karb_r.value, WS_motion_ratio_f, WS_motion_ratio_r, WD_motion_ratio_f, WD_motion_ratio_r,
                aero_load_f.value, aero_load_r.value, roll_inertia.value,
                (Csb_f/(WD_motion_ratio_f**2)), (Csr_f/(WD_motion_ratio_f**2)), (Csb_r/(WD_motion_ratio_r**2)), (Csr_r/(WD_motion_ratio_r**2)),
                (Cfb_f/(WD_motion_ratio_f**2)), (Cfr_f/(WD_motion_ratio_f**2)), (Cfb_r/(WD_motion_ratio_r**2)), (Cfr_r/(WD_motion_ratio_r**2)),
                tire_diam_f.value, tire_diam_r.value, Kt_f.value, Kt_r.value 
            )

            ssro_mod = RSF_steady_state(
                FSprungWeightDistMod, cg_height_mod.value, rc_height_f_mod.value, rc_height_r_mod.value,
                Ks_f_mod.value, Ks_r_mod.value, TotalSprungMassMod, flusm_mod.value+frusm_mod.value, rlusm_mod.value+rrusm_mod.value, GforceMod, tw_f_mod.value, tw_r_mod.value,
                Karb_f_mod.value, Karb_r_mod.value, WS_motion_ratio_f_mod, WS_motion_ratio_r_mod, WD_motion_ratio_f_mod, WD_motion_ratio_r_mod,
                aero_load_f_mod.value, aero_load_r_mod.value, roll_inertia_mod.value,
                (Csb_f_mod/(WD_motion_ratio_f_mod**2)), (Csr_f_mod/(WD_motion_ratio_f_mod**2)), (Csb_r_mod/(WD_motion_ratio_r_mod**2)), (Csr_r_mod/(WD_motion_ratio_r_mod**2)),
                (Cfb_f_mod/(WD_motion_ratio_f_mod**2)), (Cfr_f_mod/(WD_motion_ratio_f_mod**2)), (Cfb_r_mod/(WD_motion_ratio_r_mod**2)), (Cfr_r_mod/(WD_motion_ratio_r_mod**2)),
                tire_diam_f_mod.value, tire_diam_r_mod.value, Kt_f_mod.value, Kt_r_mod.value
            )
            
            segments=10*(0.1+seconds) #how many 0.1s segments are there?
            n=10000
            
            #Force Function definitions can be better packaged in function.py file, imported to the main
            if f_type == 1: #step
                force_function = np.zeros(n)
                start = int(round(n/segments, 0))
                force_function[start:n] = Gforce
                force_function_mod = np.zeros(n)
                force_function_mod[start:n] = GforceMod
            elif f_type == 2: #ramp
                force_function = np.zeros(n)
                start = int(round(n/segments, 0))
                ramp = int(round((rampT*10+1)*n/segments, 0))
                force_function[start:ramp] = np.linspace(0, Gforce, abs(start-ramp))
                force_function[ramp:n] = Gforce
                force_function_mod = np.zeros(n)
                rampMod = int(round((rampTMod*10+1)*n/segments, 0))
                force_function_mod[start:rampMod] = np.linspace(0, GforceMod, abs(start-rampMod))
                force_function_mod[rampMod:n] = GforceMod
            elif f_type == 3: #sin
                force_function = np.zeros(n)
                start = int(round(n/segments, 0))
                force_function[start:n] = Gforce*np.sin(np.linspace(0, np.pi*2*p, abs(start-n)))
                force_function_mod = np.zeros(n)
                force_function_mod[start:n] = GforceMod*np.sin(np.linspace(0, np.pi*2*pMod, abs(start-n)))
                        
            results = RSF_transient_response_6(
                force_function, seconds, #Force function(Gs, w.r.t. time) and duration(s)
                tw_f.metric(), tw_r.metric(), Ks_f.metric(), Ks_r.metric(), Karb_f.metric(), Karb_r.metric(), #track widths(m), coil(N/m) and ARB(N/m, l-r relative displacement) wheel rates
                Csb_f/(WD_motion_ratio_f**2), Csr_f/(WD_motion_ratio_f**2), Cfb_f/(WD_motion_ratio_f**2), Cfr_f/(WD_motion_ratio_f**2), Csb_r/(WD_motion_ratio_r**2), Csr_r/(WD_motion_ratio_r**2), Cfb_r/(WD_motion_ratio_r**2), Cfr_r/(WD_motion_ratio_r**2), #at-wheel damper rates(N/(m/s))
                bypassV_fb, bypassV_fr, bypassV_rb, bypassV_rr, #damper bypass speeds (m/s)
                flsm.metric(), frsm.metric(), rlsm.metric(), rrsm.metric(), flusm.metric(), frusm.metric(), rlusm.metric(), rrusm.metric(), roll_inertia.metric(), #masses (kg) and rotating inertia (kg*m**2)
                cg_height.metric(), rc_height_f.metric(), rc_height_r.metric(), tire_diam_f.metric(), tire_diam_r.metric(), #suspension geometries (m)
                WS_motion_ratio_f, WS_motion_ratio_r, WD_motion_ratio_f, WD_motion_ratio_r, #Wheel/spring or Wheel/damper motion ratios
                Kt_f.metric(), Kt_r.metric(), #tire spring rates (N/m)
                aero_load_f.metric(), aero_load_r.metric() #aerodynamic forces (N)
            )

            results_mod = RSF_transient_response_6(
                force_function_mod, seconds, #Force function(Gs, w.r.t. time) and duration(s)
                tw_f_mod.metric(), tw_r_mod.metric(), Ks_f_mod.metric(), Ks_r_mod.metric(), Karb_f_mod.metric(), Karb_r_mod.metric(), #track widths(m), coil(N/m) and ARB(N/m, l-r relative displacement) wheel rates
                Csb_f_mod/(WD_motion_ratio_f_mod**2), Csr_f_mod/(WD_motion_ratio_f_mod**2), Cfb_f_mod/(WD_motion_ratio_f_mod**2), Cfr_f_mod/(WD_motion_ratio_f_mod**2), Csb_r_mod/(WD_motion_ratio_r_mod**2), Csr_r_mod/(WD_motion_ratio_r_mod**2), Cfb_r_mod/(WD_motion_ratio_r_mod**2), Cfr_r_mod/(WD_motion_ratio_r_mod**2), #at-wheel damper rates(N/(m/s))
                bypassV_fb_mod, bypassV_fr_mod, bypassV_rb_mod, bypassV_rr_mod, #damper bypass speeds (m/s)
                flsm_mod.metric(), frsm_mod.metric(), rlsm_mod.metric(), rrsm_mod.metric(), flusm_mod.metric(), frusm_mod.metric(), rlusm_mod.metric(), rrusm_mod.metric(), roll_inertia_mod.metric(), #masses (kg) and rotating inertia (kg*m**2)
                cg_height_mod.metric(), rc_height_f_mod.metric(), rc_height_r_mod.metric(), tire_diam_f_mod.metric(), tire_diam_r_mod.metric(), #suspension geometries (m)
                WS_motion_ratio_f_mod, WS_motion_ratio_r_mod, WD_motion_ratio_f_mod, WD_motion_ratio_r_mod, #Wheel/spring or Wheel/damper motion ratios
                Kt_f_mod.metric(), Kt_r_mod.metric(), #tire spring rates (N/m)
                aero_load_f_mod.metric(), aero_load_r_mod.metric() #aerodynamic forces (N)
            )

            plt.rcParams.update({'font.size': 7})

            fig2, ([[ax0, ax1, ax2, ax3], [ax4, ax5, ax6, ax7]]) = plt.subplots(nrows=2, ncols=4, figsize=(17,10))
            fig2.suptitle(f'Lateral G Response (0-{seconds*1000}ms)')

            x = len(results[1])
            
            ax0.plot(results[0], force_function[0:x], label='Base')
            ax0.plot(results_mod[0], force_function_mod[0:x], label='Mod')
            ax0.plot(0.5, 1, 'x')
            ax0.set_ylabel('Lateral Force Function (G)')
            ax0.set_xlabel(f'(Max Values); Base:{Gforce} / Mod:{GforceMod}')
            ax0.grid()
            ax0.legend(loc=4)
            
            ax1.plot(results[0], results[1], label='Right, Base')
            ax1.plot(results[0], results[2], label='Left, Base')
            ax1.plot(results[0], (results[2]+results[1])/2, label='Center, Base')
            ax1.plot(results_mod[0], results_mod[1], label='Right, Mod')
            ax1.plot(results_mod[0], results_mod[2], label='Left, Mod')
            ax1.plot(results[0], (results_mod[2]+results_mod[1])/2, label='Center, Mod')
            ax1.set_ylabel('Total Chassis Displacement (mm)')
            ax1.set_xlabel('Test')
            ax1.grid()
            ax1.legend(loc=4)
            
            ax2.plot(results[0], results[3], label='Sprung, Base')
            ax2.plot(results[0], results[4], label='Total, Base')
            ax2.plot(results_mod[0], results_mod[3], label='Sprung, Mod')
            ax2.plot(results_mod[0], results_mod[4], label='Total, Mod')
            ax2.set_ylabel('Roll Angles (deg)')
            ax2.set_xlabel('Test')
            ax2.grid()
            ax2.legend(loc=4)

            ax3.plot(results[0], results[5], label='Front-Right, Base')
            ax3.plot(results[0], results[6], label='Front-Left, Base')
            ax3.plot(results[0], results[7], label='Rear-Right, Base')
            ax3.plot(results[0], results[8], label='Rear-Left, Base')
            ax3.plot(results_mod[0], results_mod[5], label='Front-Right, Mod')
            ax3.plot(results_mod[0], results_mod[6], label='Front-Left, Mod')
            ax3.plot(results_mod[0], results_mod[7], label='Rear-Right, Mod')
            ax3.plot(results_mod[0], results_mod[8], label='Rear-Left, Mod')
            ax3.set_ylabel('Damper Speed (mm/s)')
            ax3.set_xlabel('Test')
            ax3.grid()
            ax3.legend(loc=4)

            ax4.plot(results[0], results[9], label='Front-Right, Base')
            ax4.plot(results[0], results[10], label='Front-Left, Base')
            ax4.plot(results[0], results[11], label='Rear-Right, Base')
            ax4.plot(results[0], results[12], label='Rear-Left, Base')
            ax4.plot(results_mod[0], results_mod[9], label='Front-Right, Mod')
            ax4.plot(results_mod[0], results_mod[10], label='Front-Left, Mod')
            ax4.plot(results_mod[0], results_mod[11], label='Rear-Right, Mod')
            ax4.plot(results_mod[0], results_mod[12], label='Rear-Left, Mod')
            ax4.set_ylabel('Damper Force (N)')
            ax4.set_xlabel('Test')
            ax4.grid()
            ax4.legend(loc=4)

            ax5.plot(results[0], results[13], label='Front-Right, Base')
            ax5.plot(results[0], results[14], label='Front-Left, Base')
            ax5.plot(results[0], results[15], label='Rear-Right, Base')
            ax5.plot(results[0], results[16], label='Rear-Left, Base')
            ax5.plot(results_mod[0], results_mod[13], label='Front-Right, Mod')
            ax5.plot(results_mod[0], results_mod[14], label='Front-Left, Mod')
            ax5.plot(results_mod[0], results_mod[15], label='Rear-Right, Mod')
            ax5.plot(results_mod[0], results_mod[16], label='Rear-Left, Mod')
            ax5.set_ylabel('Tire Load (N)')
            ax5.set_xlabel('Test')
            ax5.grid()
            ax5.legend(loc=4)

            ax6.plot(results[0], results[17], label='Front, Base')
            ax6.plot(results[0], results[18], label='Rear, Base')
            ax6.plot(results_mod[0], results_mod[17], label='Front, Mod')
            ax6.plot(results_mod[0], results_mod[18], label='Rear, Mod')
            ax6.set_ylabel('Lateral Load Transfer (% Outside)')
            ax6.set_xlabel('Test')
            ax6.grid()
            ax6.legend(loc=4)

            ax7.plot(results[0], results[19], label='Base')
            ax7.plot(results_mod[0], results_mod[19], label='Mod')
            ax7.set_ylabel('Lateral Load Transfer Ratio (%)')
            ax7.set_xlabel('Test')
            ax7.grid()
            ax7.legend(loc=4)

            canvas = FigureCanvasTkAgg(fig2, master = StepWin)
            canvas.draw() 
            canvas.get_tk_widget().pack()#grid(row=0, column=0)

            def wt_Decomposition(results, results_mod, seconds):

                wt_Decomposition_win = tk.Tk()
                wt_Decomposition_win.title('Transient Lateral G Response (Base, Mod)')

                plt.rcParams.update({'font.size': 7})
                fig3, ([ax0, ax1]) = plt.subplots(nrows=2, ncols=1, figsize=(10,8))
                fig3.suptitle(f'Transient Weight Transfer by Component (0-{seconds*1000}ms)')

                ax0.plot(results[0], results[20], label='Spring, Base')
                ax0.plot(results[0], results[22], label='Anti-Roll Bar, Base')
                ax0.plot(results[0], results[9]-results[10], label='Dampers, Base')
                ax0.plot(results[0], results[24], label='Tire Damping, Base')
                ax0.plot(results[0], results[26], label='Sprung Geometric, Base')
                ax0.plot(results[0], results[28], label='Unsprung Geometric, Base')
                ax0.plot(results_mod[0], results_mod[20], label='Spring, Mod')
                ax0.plot(results_mod[0], results_mod[22], label='Anti-Roll Bar, Mod')
                ax0.plot(results_mod[0], results_mod[9]-results_mod[10], label='Dampers, Mod')
                ax0.plot(results_mod[0], results_mod[24], label='Tire Damping, Mod')
                ax0.plot(results_mod[0], results_mod[26], label='Sprung Geometric, Mod')
                ax0.plot(results_mod[0], results_mod[28], label='Unsprung Geometric, Mod')
                ax0.set_ylabel('Weight Transfer by Component, Front (N)')
                ax0.set_xlabel('Test')
                ax0.grid()
                ax0.legend(loc=4)

                ax1.plot(results[0], results[21], label='Spring, Base')
                ax1.plot(results[0], results[23], label='Anti-Roll Bar, Base')
                ax1.plot(results[0], results[11]-results[12], label='Dampers, Base')
                ax1.plot(results[0], results[25], label='Tire Damping, Base')
                ax1.plot(results[0], results[27], label='Sprung Geometric, Base')
                ax1.plot(results[0], results[29], label='Unsprung Geometric, Base')
                ax1.plot(results_mod[0], results_mod[21], label='Spring, Mod')
                ax1.plot(results_mod[0], results_mod[23], label='Anti-Roll Bar, Mod')
                ax1.plot(results_mod[0], results_mod[11]-results_mod[12], label='Dampers, Mod')
                ax1.plot(results_mod[0], results_mod[25], label='Tire Damping, Mod')
                ax1.plot(results_mod[0], results_mod[27], label='Sprung Geometric, Mod')
                ax1.plot(results_mod[0], results_mod[29], label='Unsprung Geometric, Mod')
                ax1.set_ylabel('Weight Transfer by Component, Raer (N)')
                ax1.set_xlabel('Test')
                ax1.grid()
                ax1.legend(loc=4)

                canvas = FigureCanvasTkAgg(fig3, master = wt_Decomposition_win)
                canvas.draw() 
                canvas.get_tk_widget().pack()

                wt_Decomposition_win.mainloop()

            weight_trans_decomp_button = tk.Button(StepWin, fg='blue', text = "Weight Transfer by Component", command = lambda: wt_Decomposition(results, results_mod, seconds), width=34)
            weight_trans_decomp_button.pack()#grid(row=1, column=0)

            stats_button = tk.Button(StepWin, fg='blue', text = "Detailed Base/Mod Statistics", width=34)
            stats_button.pack()#grid(row=1, column=0)

            stats_button = tk.Button(StepWin, fg='blue', text = "Debug Variables and Development (Beta)", width=34)
            stats_button.pack()#grid(row=1, column=0)

            StepWin.mainloop()

        #BUTTONS=================================================================================================================
        LabelM = tk.Label(root, text='     ')
        LabelM.grid(row=94, column=4)

        DamperPlotButton = tk.Button(root, fg='blue', text = "User Guide", width=16)
        DamperPlotButton.grid(row=131, column=0)

        DamperPlotButton = tk.Button(root, fg='blue', command = DamperPlots , text = "Damper Plots", width=16)
        DamperPlotButton.grid(row=132, column=0)

        CalculateButton = tk.Button(root, text='Basic Parameters', command=RollSimMain, fg='blue', width=16)
        CalculateButton.grid(row=133, column=0)

        DamperPlotButton = tk.Button(root, fg='blue', text = "Roll Response (Step)", command = lambda: Resp3(1), width=16)
        DamperPlotButton.grid(row=134, column=0)

        DamperPlotButton = tk.Button(root, fg='blue', text = "Roll Response (Ramp)", command = lambda: Resp3(2), width=16)
        DamperPlotButton.grid(row=135, column=0)
        
        DamperPlotButton = tk.Button(root, fg='blue', text = "Roll Response (Sin)", command = lambda: Resp3(3), width=16)
        DamperPlotButton.grid(row=136, column=0)

        LabelM = tk.Label(root, text='     ').grid(row=137, column=0)
        
        root.mainloop()

    def S():
        safetyWarning = tk.Tk()
        safetyWarning.title('Safety Warning')
        
        Label3 = tk.Label(safetyWarning, wraplength=400, justify="left",
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
        LL = tk.Tk()
        LL.title('Release of Liability')
        
        Label3 = tk.Label(LL, wraplength=400, justify="left",
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
        
    SButton = tk.Button(safety, command=S, text = """Safety Warning""", width=16)
    SButton.grid(row=5, column=0)

    LLButton = tk.Button(safety, command=LL, text = """Release of Liability""", width=16)
    LLButton.grid(row=7, column=0)

    Label3 = tk.Label(safety, wraplength=400, justify="center",
                text=""" """).grid(row=8, column=0)

    Label3 = tk.Label(safety, wraplength=400, justify="center",
                text="""By clicking the button below and continuing to Roll.Sim, you, the user, certify that you have carefully read, understood, and agree to the Release of Liability Statement and Safety Warning of your own free will.""").grid(row=9, column=0)

    Label3 = tk.Label(safety, wraplength=400, justify="center",
                text=""" """).grid(row=12, column=0)

    HomeButton = tk.Button(safety, command=Home, wraplength=250, fg='white', bg='red', text = """I have read, understand, and agree to the safety warning and release of liability above.""")
    HomeButton.grid(row=11, column=0)

    safety.mainloop()