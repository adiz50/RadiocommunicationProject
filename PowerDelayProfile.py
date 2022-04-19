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
time_and_power_before_normalization = []
x = np.linspace(0.0, calc.width,samples_init)

#for i in range(samples_init):

    #P1 = (1 / calc.los_length(x[i])) ** 2  # LOS

    #P2 = (calc.reflectance(calc.wall_once_reflected_path_length_and_angle(x[i])[1], wood) /
       #   calc.wall_once_reflected_path_length_and_angle(x[i])[0]) ** 2
    #P3 = (calc.reflectance(calc.ceiling_once_reflected_path_length_and_angle(x[i])[1], concrete) /
      #    calc.ceiling_once_reflected_path_length_and_angle(x[i])[0]) ** 2

    #P4 = ((calc.reflectance(calc.wall_reflected_twice(x[i])[1], wood) * calc.reflectance(calc.wall_reflected_twice(x[i])[1], concrete)) /
     #     calc.wall_reflected_twice(x[i])[0]) ** 2
    #P5 = ((calc.reflectance(calc.ceiling_reflected_twice(x[i])[1], glass) * calc.reflectance(calc.ceiling_reflected_twice(x[i])[1], concrete)) /
        #  calc.ceiling_reflected_twice(x[i])[0]) ** 2


    #if i==0:
    #    time_normalized.append(0)
    #    power_normalized.append(1)
    #    i+=1
    #TIME NORMALIZED POWER NORMALIZED
    #temporary_time_value = calc.los_length(x[0])/c
    #temporary_power_value = (1 / calc.los_length(x[0]))
    #print("czas 0",temporary_time_value)
    #print(calc.los_length(x[i]) / c)
    #LO
    #time_normalized.append((((calc.los_length(x[i])/c))-temporary_time_value)*s_to_ns)
    #power_normalized.append(P1/temporary_power_value)

    #Multipath reflected wall
    #time_normalized.append((((calc.wall_once_reflected_path_length_and_angle(x[i])[0])/c)
    #                                               -temporary_time_value)*s_to_ns)
    #power_normalized.append(P2 / temporary_power_value)

    #Multipath reflected ceiling
    #time_normalized.append((((calc.ceiling_once_reflected_path_length_and_angle(x[i])[0])/c)
    #                                        -temporary_time_value)*s_to_ns)
    #power_normalized.append(P3 / temporary_power_value)

    #Multipath reflected wall twice
    #time_normalized.append((((calc.wall_reflected_twice(x[i])[0])/c)-temporary_time_value)*s_to_ns)
    #power_normalized.append(P4 / temporary_power_value)

    #multipath reflected ceiling twice
    #time_normalized.append((((calc.ceiling_reflected_twice(x[i])[0])/c)-temporary_time_value)*s_to_ns)
    #power_normalized.append(P5/temporary_power_value)


    #np.append(time_and_power_before_normalization,[[(calc.los_length(x[i])/c),(P1)]],axis=0)

    #np.append(time_and_power_before_normalization, [[(calc.wall_once_reflected_path_length_and_angle(x[i][0]) / c), (P2)]],
    #          axis=0)

    #np.append(time_and_power_before_normalization, [[(calc.ceiling_once_reflected_path_length_and_angle(x[i][0]) / c), (P3)]],
    #          axis=0)

    #np.append(time_and_power_before_normalization, [[(calc.wall_reflected_twice(x[i][0]) / c), (P4)]],
    #          axis=0)

    #np.append(time_and_power_before_normalization, [[(calc.wall_reflected_twice(x[i][0]) / c), (P5)]],
    #          axis=0)
#print(time_normalized)

for i in range(samples_init):
    path_wall_once, angles_wall_once = calc.wall_once_reflected_path_length_and_angle(x[i])
    path_ceiling_once, angles_ceiling_once = calc.ceiling_once_reflected_path_length_and_angle(x[i])
    path_wall_twice, angles_wall_twice = calc.wall_reflected_twice(x[i])
    path_ceiling_twice, angles_ceiling_twice = calc.ceiling_reflected_twice(x[i])

    P1 = (1 / calc.los_length(x[i])) ** 2  # LOS

    P2 = (calc.reflectance(angles_wall_once, wood) / path_wall_once) ** 2
    P3 = (calc.reflectance(angles_ceiling_once, concrete) / path_ceiling_once) ** 2

    P4 = ((calc.reflectance(angles_wall_twice, wood) * calc.reflectance(angles_wall_twice, concrete)) /path_wall_twice) ** 2

    P5 = ((calc.reflectance(angles_ceiling_twice, glass) * calc.reflectance(angles_ceiling_twice, concrete)) / path_ceiling_twice) ** 2

    for m in range(1):
        time_and_power_before_normalization.append([(calc.los_length(x[i])/c),(P1)])

        time_and_power_before_normalization.append([(path_wall_once / c), (P2)])

        time_and_power_before_normalization.append([(path_ceiling_once / c), (P3)])

        time_and_power_before_normalization.append([(path_wall_twice / c), (P4)])

        time_and_power_before_normalization.append([(path_ceiling_twice / c), (P5)])






time_and_power_before_normalization.sort(key=lambda x:x[0])
#print(np.matrix(time_and_power_before_normalization))

temporary_time_value = time_and_power_before_normalization[0][0]
temporary_power_value = time_and_power_before_normalization[0][1]

#print(np.hsplit(time_and_power_before_normalization,2))
#power_normalized.append(np.hsplit(time_and_power_before_normalization,1)[1])

for n in range(samples_init):
    if n==0:
        time_and_power_before_normalization[0][0] = 0
        time_and_power_before_normalization[0][1] = 1
        n+=1

    time_and_power_before_normalization[n][0] = (time_and_power_before_normalization[n][0] - temporary_time_value) * s_to_ns
    time_and_power_before_normalization[n][1] = (time_and_power_before_normalization[n][1] / temporary_power_value)

print(np.matrix(time_and_power_before_normalization))
# plt.xlabel("time delay [ns]")
# plt.ylabel("normalized power")
plt.plot(time_and_power_before_normalization)
plt.show()