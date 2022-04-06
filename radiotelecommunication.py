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
from matplotlib.widgets import Slider, Button

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

def LOS_length(x):
    if (x > width / 2):
        x = -x + width
    los = math.sqrt((width / 2 - x) ** 2 + (length - 0.5) ** 2)
    # los = math.sqrt(los)
    return los


def wall_once_reflected_path_length_and_angle(x):

    if x < width / 2:
        x = -x + width
    a2_side = ((length-0.5)*width/2)/(x+width/2)
    a1_side = length-0.5-a2_side
    c1_side = math.sqrt(a1_side**2 + x**2)
    c2_side = math.sqrt(a2_side**2 + (width/2)**2)

    path = c1_side + c2_side
    angle = math.asin(x/c1_side)

    return path, angle

def ceiling_once_reflected_path_length_and_angle(x):
    los = LOS_length(x)
    path = math.sqrt((height*2)**2+los**2)
    angle = math.asin(height*2/path)

    return path, angle

for i in range(samples_init):
    los_left = LOS_length(x1[i])
    los.append(los_left)
    multipath_wall, multipath_wall_angle = wall_once_reflected_path_length_and_angle(x1[i])
    multipath_ceiling, multipath_ceiling_angle = ceiling_once_reflected_path_length_and_angle(x1[i])
    wall.append(multipath_wall)
    angles_wall.append(multipath_wall_angle)
    ceiling.append(multipath_ceiling)
    angles_ceiling.append(multipath_ceiling_angle)



# for i in range(100):
#    los_right = LOS_length(x2[i])
#    los.append(los_right)
# print(los_right)
def reflectance(angle):
    a = (math.cos(angle) - math.sqrt(concrete - math.sin(angle) ** 2)) / (
                math.cos(angle) + math.sqrt(concrete - math.sin(angle) ** 2))
    return a

def diffraction():

    v = h*math.sqrt((2/lam)*(s1s2)/(r1*r2))
    diff = 6.9+20*math.log10(math.sqrt((v-0.1)**2+1)+v-0.1)

    return diff

def received_power_multipath1(path_los, path_wall, path_ceiling, array, samples):
    for x in range(samples):
        fi1 = -1 * (2 * pi * fc * path_los[x]) / light
        fi2 = -1 * (2 * pi * fc * path_wall[x]) / light
        fi3 = -1 * (2 * pi * fc * path_ceiling[x]) / light

        P1 = (1 / path_los[x]) * cmath.exp(pi * fi1 * 1j)  # LOS
        P2 = (reflectance(angles_wall[x]) / path_wall[x]) * cmath.exp(pi * fi2 * 1j)  # Reflected path wall
        P3 = (reflectance(angles_ceiling[x]) / path_ceiling[x]) * cmath.exp(pi * fi3 * 1j)  # Reflected path ceiling
        sum = 10*math.log10(abs(P1 + P2 + P3) ** 2)
        array.append(sum)
        if(x==601):
            print(sum)
            print(reflectance(angles_wall[x]),angles_wall[x])
            print(reflectance(angles_ceiling[x]),angles_ceiling[x])



    return array


def received_power_los(path, array, samples):
    for x in range(samples):
        fi = -1 * (2 * pi * fc * path[x]) / light
        P = 10*math.log10(abs((1 / path[x]) * cmath.exp(pi * fi * 1j)) ** 2)
        array.append(P)
    return array


LOS_line = received_power_los(los, PrP0_los,samples_init)
multipath = received_power_multipath1(los, wall, ceiling, PrP0_multipath,samples_init)


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
