# Roll.Sim
Hello! Thank you for visiting Roll.Sim, a chassis response simulator written in Python, solving with multi-body physics and 4th-order Runge-Kutta methods. Roll.Sim is designed to be more lightweight and inexpensive than professional chassis simulation software, while still being far more detailed and descriptive than traditional grassroots motorsports tuning tools.

Please note! Roll.Sim is currently published without any license, and is for viewing only, with no rights granted for public use, distribution, or modification. For your own safety, please do not use or borrow Roll.Sim code as it is still highly experimental.

## Areas of Active Development
1. Func_time_response_VI.py, containing the function RSF_transient_response_VI(): This is the latest version of the transient roll response calculator, the heart of Roll.Sim. This vehicle model represents a step-change in accuracy over version V allowing for asymmetric roll brought on by different bound/rebound damper rates on the outside/inside wheels, respectively. DOFs increase from 3 to 6. This function will also include functionality to decompose weight transfer by components (sprung/unsprung geometric, springs, anti-roll bars, dampers, etc).
2. General cleanup: includes import statement cleanup, resolving old comments, unifying naming conventions, etc.
