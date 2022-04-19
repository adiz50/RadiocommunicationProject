import calculator as calc
import math
import numpy as np
from calculator import wood, glass, concrete
import matplotlib.pyplot as plt

length = 5
height = 2.5
width = 4

samples_init = 2000

concrete = 5.31
c = 3e8
fc = 2.4e9
lam = c / fc
s_to_ns = 10e9

time_normalized = []
power_normalized = []

x = np.linspace(0.0, calc.width,samples_init)

for i in range(samples_init):

    P1 = (1 / calc.los_length(x[i])) ** 2  # LOS

    P2 = (calc.reflectance(calc.wall_once_reflected_path_length_and_angle(x[i])[1], wood) /
          calc.wall_once_reflected_path_length_and_angle(x[i])[0]) ** 2
    P3 = (calc.reflectance(calc.ceiling_once_reflected_path_length_and_angle(x[i])[1], concrete) /
          calc.ceiling_once_reflected_path_length_and_angle(x[i])[0]) ** 2

    P4 = ((calc.reflectance(calc.wall_reflected_twice(x[i])[1], wood) * calc.reflectance(calc.wall_reflected_twice(x[i])[1], concrete)) /
          calc.wall_reflected_twice(x[i])[0]) ** 2
    P5 = ((calc.reflectance(calc.ceiling_reflected_twice(x[i])[1], glass) * calc.reflectance(calc.ceiling_reflected_twice(x[i])[1], concrete)) /
          calc.ceiling_reflected_twice(x[i])[0]) ** 2


    if i==0:
        time_normalized.append(0)
        power_normalized.append(1)
        i+=1
    #TIME NORMALIZED POWER NORMALIZED
    temporary_time_value = calc.los_length(x[0])/c
    temporary_power_value = (1 / calc.los_length(x[0]))
    print("czas 0",temporary_time_value)
    print(calc.los_length(x[i]) / c)
    #LO
    time_normalized.append((((calc.los_length(x[i])/c))-temporary_time_value)*s_to_ns)
    power_normalized.append(P1/temporary_power_value)
    #Multipath reflected wall
    time_normalized.append((((calc.wall_once_reflected_path_length_and_angle(x[i])[0])/c)
                                                   -temporary_time_value)*s_to_ns)
    power_normalized.append(P2 / temporary_power_value)
    #Multipath reflected ceiling
    time_normalized.append((((calc.ceiling_once_reflected_path_length_and_angle(x[i])[0])/c)
                                            -temporary_time_value)*s_to_ns)
    power_normalized.append(P3 / temporary_power_value)
    #Multipath reflected wall twice
    time_normalized.append((((calc.wall_reflected_twice(x[i])[0])/c)-temporary_time_value)*s_to_ns)
    power_normalized.append(P4 / temporary_power_value)
    #multipath reflected ceiling twice
    time_normalized.append((((calc.ceiling_reflected_twice(x[i])[0])/c)-temporary_time_value)*s_to_ns)
    power_normalized.append(P5/temporary_power_value)
#print(time_normalized)
#time_normalized_power_normalized.sort(key=lambda x:x[1])
#plt.xlabel("time delay [ns]")
#plt.ylabel("normalized power")
#plt.plot(time_normalized,power_normalized)
#plt.show()
