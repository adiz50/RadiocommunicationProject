import calculator as calc
import math
import numpy as np

length = 5
height = 2.5
width = 4

samples_init = 2000

concrete = 5.31
light = 3e8
fc = 2.4e9
lam = light / fc

#los = []
#wall = []
#ceiling = []
power_los = []
power2 = []
power3 = []
power4 = []
power5 = []

time1 = []
time2 = []
time3 = []
time4 = []
time5 = []

x = np.linspace(0.0, calc.width,samples_init)

for i in range(samples_init):





    P1 = (1 / calc.path_los(x[i])) ** 2  # LOS

    P2 = (calc.reflectance(calc.wall_once_reflected_path_length_and_angle(x[i])[1], wood) /
          calc.wall_once_reflected_path_length_and_angle(x[i])[0]) ** 2
    P3 = (calc.reflectance(calc.ceiling_once_reflected_path_length_and_angle(x[i])[1], concrete) /
          calc.ceiling_once_reflected_path_length_and_angle(x[i])[0]) ** 2

    P4 = ((calc.reflectance(calc.wall_reflected_twice(x[i])[1], wood) * calc.reflectance(calc.wall_reflected_twice(x[i])[1], concrete)) /
          calc.wall_reflected_twice(x[i])[0]) ** 2
    P5 = ((calc.reflectance(calc.ceiling_reflected_twice(x)[1], glass) * calc.reflectance(calc.ceiling_reflected_twice(x[i])[1], concrete)) /
          calc.ceiling_reflected_twice(x[i])[0]) ** 2

    time1[0].append(0)
    time1.append(calc.path_los(x[i])/c)
    time2.append((calc.wall_once_reflected_path_length_and_angle(x[i])[0])/c)
    time3.append((calc.ceiling_once_reflected_path_length_and_angle(x[i])[0])/c)
    time4.append((calc.wall_reflected_twice(x[i])[0])/c)
    time5.append((calc.ceiling_reflected_twice(x[i])[0])/c)

