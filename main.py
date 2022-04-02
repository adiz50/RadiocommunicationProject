import cmath
import math
from cmath import pi

import matplotlib.pyplot as plt
import numpy as np

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

lenght = 5
height = 2.5
width = 4

concrete = 5.31
light = 3 * 10 ** 8
fc = 2.4 * 10 ** 9
lam = light / fc


def LOS_length(point):
    if point == 0:
        los = 4.5
    los = point ** 2 + (4.5) ** 2
    los = math.sqrt(los)
    return los


x1 = np.linspace(2.0, 0.0, 100)
x2 = np.linspace(0.02, 2.0, 100)
los = []
PrP0 = []
for i in range(100):
    los_left = LOS_length(x1[i])
    los.append(los_left)
    # print(los_left)

for i in range(100):
    los_right = LOS_length(x2[i])
    los.append(los_right)
    # print(los_right)


def received_power_los(path, array):
    i = len(path)
    for x in range(i):
        fi = -1 * (2 * pi * fc * path[x]) / light
        P = abs((1 / path[x]) * cmath.exp(pi * fi * 1j)) ** 2
        array.append(P)
    return array


dupa = received_power_los(los, PrP0)
plt.plot(dupa)
plt.show()
# print(x1)
# print(x2)
