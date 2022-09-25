import numpy as np
import pandas as pd

def RSF_force_function(
    seconds, f_type, g_force, g_force_mod, ramp_time, ramp_time_mod, period, period_mod, path
):

    segments=10*(0.1+seconds) #how many 0.1s segments are there?
    n=10000 #takes 0.8s to iterate through 10k rows
    
    #Force Function definitions can be better packaged in function.py file, imported to the main
    if f_type == 1: #step
        force_function = np.zeros(n)
        start = int(round(n/segments, 0))
        force_function[start:n] = g_force 
        force_function_mod = np.zeros(n)
        force_function_mod[start:n] = g_force_mod

    elif f_type == 2: #ramp
        force_function = np.zeros(n)
        start = int(round(n/segments, 0))
        ramp = int(round((ramp_time*10+1)*n/segments, 0))
        force_function[start:ramp] = np.linspace(0, g_force, abs(start-ramp))
        force_function[ramp:n] = g_force
        force_function_mod = np.zeros(n)
        rampMod = int(round((ramp_time_mod*10+1)*n/segments, 0))
        force_function_mod[start:rampMod] = np.linspace(0, g_force_mod, abs(start-rampMod))
        force_function_mod[rampMod:n] = g_force_mod

    elif f_type == 3: #sin
        force_function = np.zeros(n)
        start = int(round(n/segments, 0))
        force_function[start:n] = g_force*np.sin(np.linspace(0, np.pi*2*period, abs(start-n)))
        force_function_mod = np.zeros(n)
        force_function_mod[start:n] = g_force_mod*np.sin(np.linspace(0, np.pi*2*period_mod, abs(start-n)))

    elif f_type == 4: #from telemetry
        df = pd.read_csv(path)
        force_function = force_function_mod = df['g_force_x'].to_numpy()
        seconds = len(force_function)/1000
    
    return(
        force_function, force_function_mod, seconds
    )