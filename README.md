# Roll.Sim

![main](https://github.com/iPandev/Roll.Sim/blob/main/workflows/pytest_windows.yml/badge.svg)

Hello! Thank you for visiting Roll.Sim, a chassis response simulator solving with multi-body physics and 4th-order Runge-Kutta methods. Roll.Sim is designed to be more lightweight and inexpensive than professional chassis simulation software, while still being far more detailed and descriptive than traditional grassroots motorsports tuning tools. Please note that Roll.Sim is, for now, published without any license, and is for viewing only, with no rights granted for public use, distribution, or modification. 

## Safety
For your own safety, DO NOT use Roll.Sim code on real-world vehicles as it is still highly experimental.

## Areas of Active Development
1. Func_time_response_VI.py, containing the function RSF_transient_response_VI(): This is the latest version of the transient roll response calculator, the heart of Roll.Sim. The updated vehicle model represents a step-change in accuracy over version V allowing for asymmetric roll brought on by different bound/rebound damper rates on the outside/inside wheels, respectively. DOFs increase from 3 to 6. This function will also include functionality to decompose weight transfer by components (sprung/unsprung geometric, springs, anti-roll bars, dampers, etc), which will need to be supported in the main Roll.Sim file. For more information on the new vehicle model, view RollSim_vehicle_model_a.jpg and RollSim_vehicle_model_b.jpg. The notation is as follows: "a" and "b" variables describe chassis displacement and tire displacement, respectively. "I" represents rotational inertia about the roll axis, "USM" variables represent unsprung masses. "K" and "C" variables represent spring and damper rates, respectively. Equations 1b, 2b, and 3-6 compose the complete set of differential equations to be solved using RK4, from which time-dependent tire loads can be explicitly derived.

2. General cleanup: includes import statement cleanup, resolving old comments, unifying naming conventions, etc.
