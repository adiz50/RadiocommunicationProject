import cmath
import math
from cmath import pi

import matplotlib.pyplot as plt
import numpy as np

import calculator as calc

# fi = -(2*pi*fc*di)/light

# power = abs(E^n*ai/di*e^jfi)^2

# reflectance depends on an angle so we also have to calculate it for different points of measurement
# a = (cos(x)-sqrt(n-sin(x)^2))/(cos(x)+sqrt(n-sin(x)^2))

# Deugant model for diffraction
# v = h*sqrt((2/lam)*(s1+s2/r1*r2))
# C = 6.9+20*log(sqrt((v-0.1)^2+1)+v-0.1)

##############
#  .        # #
#   .       #  #
###########    #
#   .      #   #
#   .      #   #
#   .      #   #
#   .      #   #
#   . .... #.. #
# .        #  #
#############

length = 5
height = 2.5
width = 4

samples_init = 2000

concrete = 5.31
light = 3e8
fc = 2.4e9
lam = light / fc

los = []
wall = []
ceiling = []
PrP0_los = []
PrP0_multipath = []
current_angle = []
angles_ceiling = []
angles_wall = []

x1 = np.linspace(0.0, 4.0, samples_init)

for i in range(samples_init):
    los_left = calc.los_length(x1[i])
    los.append(los_left)
    multipath_wall, multipath_wall_angle = calc.wall_once_reflected_path_length_and_angle(x1[i])
    multipath_ceiling, multipath_ceiling_angle = calc.ceiling_once_reflected_path_length_and_angle(x1[i])
    wall.append(multipath_wall)
    angles_wall.append(multipath_wall_angle)
    ceiling.append(multipath_ceiling)
    angles_ceiling.append(multipath_ceiling_angle)


# for i in range(100):
#    los_right = LOS_length(x2[i])
#    los.append(los_right)
# print(los_right)


# def diffraction():
#
#     v = h*math.sqrt((2/lam)*(s1+s2)/(r1*r2))
#     diff = 6.9+20*math.log10(math.sqrt((v-0.1)**2+1)+v-0.1)
#
#     return diff
# TODO errory tu są

plt.xlabel('Distance from the left wall [cm]')
plt.ylabel('Pr/P0')
# y is distance from the transmitter
plt.plot(LOS_line, label="LOS line")
plt.plot(multipath, label="Multipath 1")

plt.title('Multipath fading')
# show a legend on the plot
plt.legend()
# Display a figure.
plt.show()
