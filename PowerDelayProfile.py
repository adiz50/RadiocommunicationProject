from decimal import *

import matplotlib.pyplot as plt
import numpy as np

import calculator as calc
from calculator import wood, glass
from matplotlib.widgets import Slider

length = 5
height = 2.5
width = 4

samples_init = 1

concrete = 5.31
c = 3e8
fc = 2.4e9
lam = c / fc
s_to_ps = 10e12

time_normalized = []
power_normalized = []
time_and_power_before_normalization = []
x = np.linspace(1.0, calc.width / 2, samples_init)


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
                                                             temporary_time_value) * 10 ** 12)

        time_and_power_before_normalization[n][1] = (time_and_power_before_normalization[n][1] / temporary_power_value)

        # print(np.matrix(time_and_power_before_normalization))

    return time_and_power_before_normalization


fig = plt.figure()
ax = fig.subplots()
plt.subplots_adjust(bottom=0.25)
p = ax.bar(*zip(*power_delay_profile(1)), width=100)
plt.title("Power delay profile")
plt.xlabel("Time delay [ns]")
plt.ylabel("Normalized power")

ax_slider = plt.axes([0.1, 0.1, 0.8, 0.05], facecolor='green')
slider = Slider(ax_slider, "Distance from left wall", valmin=0, valmax=4, valinit=0, valstep=0.1)


def update_line(val):
    print(slider.val)
    p.bar(*zip(*power_delay_profile(slider.val)), width=100)
    plt.show()
    fig.canvas.draw()


slider.on_changed(update_line)

plt.show()

# TODO odbiornik i nadajnik na 1m wysokości
# TODO ogarnąć wykres PDP
