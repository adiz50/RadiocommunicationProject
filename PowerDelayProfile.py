import math
from decimal import *
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import calculator as calc
from calculator import wood, glass



length = 5
height = 2.5
width = 4

samples_init = 1

concrete = 5.31
c = 3e8
fc = 2.4e9
lam = c / fc
s_to_ps = 10e9
#select position between 0 and 4 that indicates your place in the room
d = 1
time_normalized = []
power_normalized = []
time_and_power_before_normalization = []
# time_avg_squared = []
# values= []
# #time_avg = []

def power_delay_profile(x):
    path_wall_once, angles_wall_once = calc.wall_once_reflected_path_length_and_angle(x)
    path_ceiling_once, angles_ceiling_once = calc.ceiling_once_reflected_path_length_and_angle(x)
    path_wall_twice, angles_wall_twice = calc.wall_reflected_twice(x)
    path_ceiling_twice, angles_ceiling_twice = calc.ceiling_reflected_twice(x)

    P1 = (1 / calc.los_length(x)) ** 2  # LOS

    P2 = (calc.reflectance(angles_wall_once, wood) / path_wall_once) ** 2
    P3 = (calc.reflectance(angles_ceiling_once, concrete) / path_ceiling_once) ** 2

    P4 = ((calc.reflectance(angles_wall_twice, wood) * calc.reflectance(angles_wall_twice,
                                                                        concrete)) / path_wall_twice) ** 2

    P5 = ((calc.reflectance(angles_ceiling_twice, glass) * calc.reflectance(angles_ceiling_twice,
                                                                            concrete)) / path_ceiling_twice) ** 2

    time_and_power_before_normalization.append([(calc.los_length(x) / c), P1])

    time_and_power_before_normalization.append([(path_wall_once / c), P2])

    time_and_power_before_normalization.append([(path_ceiling_once / c), P3])

    time_and_power_before_normalization.append([(path_wall_twice / c), P4])

    time_and_power_before_normalization.append([(path_ceiling_twice / c), P5])

    time_and_power_before_normalization.sort(key=lambda x: x[0])

    temporary_time_value = Decimal(time_and_power_before_normalization[0][0])
    temporary_power_value = time_and_power_before_normalization[0][1]
    getcontext().prec = 15

    for n in range(len(time_and_power_before_normalization)):
        # print(time_and_power_before_normalization[n][0], " - ", temporary_time_value)
        # print(time_and_power_before_normalization[n][0],"-",temporary_time_value)
        time_and_power_before_normalization[n][0] = Decimal(time_and_power_before_normalization[n][0])
        time_and_power_before_normalization[n][0] = (Decimal(time_and_power_before_normalization[n][0] -
                                                             temporary_time_value) * 10 ** 9)

        time_and_power_before_normalization[n][1] = (time_and_power_before_normalization[n][1] / temporary_power_value)

        print(np.matrix(time_and_power_before_normalization))

    return time_and_power_before_normalization

# for n in range(len(time_and_power_before_normalization)):
#
#     time_avg.append(time_and_power_before_normalization[n][0]*time_and_power_before_normalization[n][1])
#
#     values.append(time_and_power_before_normalization[n][1])
#
#     time_avg_squared.append((time_and_power_before_normalization[n][0]**2) * time_and_power_before_normalization[n][1])
#
#print(np.matrix(time_and_power_before_normalization))
# tau_rms = math.sqrt((sum(time_avg_squared)/sum(values)-(sum(time_avg)/sum(values)**2)))
# print(tau_rms)
plt.bar(*zip(*power_delay_profile(d)), width = 0.2)
plt.title("Power delay profile "+str(d)+"m from the left wall")
plt.xlabel("Time delay [ns]")
plt.ylabel("Normalized power")


plt.show()

# TODO odbiornik i nadajnik na 1m wysokości
# TODO ogarnąć wykres PDP
