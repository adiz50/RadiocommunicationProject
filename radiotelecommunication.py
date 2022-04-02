from cmath import pi, sin
import platform
import sys
import os
import datetime
import hashlib
import cmath
import math
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import imageio
from scipy import signal

# fi = -(2*pi*fc*di)/light

# power = abs(E^n*ai/di*e^jfi)^2

# reflectance depends on an angle so we also have to calculate it for different points of measurement
# a = (cos(x)-sqrt(n-sin(x)^2))/(cos(x)+sqrt(n-sin(x)^2))

# Deugant model for diffraction
# v = h*sqrt((2/lam)*(s1+s2/r1*r2))
# C = 6.9+20*log(sqrt((v-0.1)^2+1)+v-0.1)

#############
# .        # #
#  .      #   #
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

samples = 200

concrete = 5.31
light = 3 * 10 ** 8
fc = 2.4 * 10 ** 9
lam = light / fc


def LOS_length(x):
    if (x > width / 2):
        x = -x + width
    los = math.sqrt((width / 2 - x) ** 2 + (length - 0.5) ** 2)
    # los = math.sqrt(los)
    return los


x1 = np.linspace(0.0, 4.0, samples)
# x2 = np.linspace(0.02, 2.0, num = 100)
los = []
PrP0_los = []
PrP0_multipath = []
current_angle = []
angles_ceiling = []
angles_wall = []
for i in range(samples):
    los_left = LOS_length(x1[i])
    los.append(los_left)
    # print(los_left)


# for i in range(100):
#    los_right = LOS_length(x2[i])
#    los.append(los_right)
# print(los_right)
def reflectance(angle):
    a = (math.cos(angle) - math.sqrt(concrete - math.sin(angle) ** 2)) / (
                math.cos(angle) + math.sqrt(concrete - math.sin(angle) ** 2))
    return a


def received_power_multipath1(path_los, path_wall, path_ceiling, array):
    i = samples
    for x in range(i):
        fi1 = -1 * (2 * pi * fc * path_los[x]) / light
        fi2 = -1 * (2 * pi * fc * path_wall[x]) / light
        fi3 = -1 * (2 * pi * fc * path_ceiling[x]) / light

        P1 = (1 / path_los[x]) * cmath.exp(pi * fi1 * 1j)  # LOS
        P2 = (reflectance(angles_wall[x]) / path_wall[x]) * cmath.exp(pi * fi2 * 1j)  # Reflected path wall
        P3 = (reflectance(angles_ceiling[x]) / path_ceiling[x]) * cmath.exp(pi * fi3 * 1j)  # Reflected path ceiling
        sum = abs(P1 + P2 + P3) ** 2
        array.append(sum)
    return array


def received_power_los(path, array):
    i = samples
    for x in range(i):
        fi = -1 * (2 * pi * fc * path[x]) / light
        P = abs((1 / path[x]) * cmath.exp(pi * fi * 1j)) ** 2
        array.append(P)
    return array


LOS_line = received_power_los(los, PrP0_los)
multipath = received_power_multipath1(los, PrP0_multipath)

# y is distance from the transmitter
plt.plot(LOS_line, label="LOS line")
plt.plot(multipath, label="Multipath 1")

plt.title('Multipath fading')
# show a legend on the plot
plt.legend()
# Display a figure.
plt.show()
