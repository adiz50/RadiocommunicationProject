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

LOS_line = []
multipath1 = []
multipath2 = []
diffracted_line = []

x = np.linspace(0.0, calc.width, samples_init)
x1 = np.linspace(0.0, calc.width + calc.additional_room_width, samples_init)

for i in range(samples_init):

    #LOS_line.append(calc.received_power_los(x[i]))
    #multipath1.append(calc.received_power_multipath1(x[i]))
    #multipath2.append(calc.received_power_multipath2(x[i]))
    if not calc.is_it_diffraction(x1[i]):
        diffracted_line.append(calc.received_power_los(x1[i]))
        LOS_line.append(calc.received_power_los(x1[i]))
        multipath1.append(calc.received_power_multipath1(x1[i]))
        multipath2.append(calc.received_power_multipath2(x1[i]))
        #diffracted_line.append(0)
    elif calc.is_it_diffraction(x1[i]):
        diffracted_line.append(calc.diffraction(x1[i]))
        LOS_line.append(None)
        multipath1.append(None)
        multipath2.append(None)

plt.xlabel('Distance from the left wall [cm]')
plt.ylabel('Pr/P0 [dB]')
# y is distance from the transmitter
plt.plot(x1 * 100, LOS_line, label="LOS line")
plt.plot(x1 * 100, multipath1, label="Multipath 1")
plt.plot(x1 * 100, multipath2, label="Multipath 2")
plt.plot(x1 * 100, diffracted_line, label="Diffracted line")

plt.title('Multipath fading')
# show a legend on the plot
plt.legend()
# Display a figure.
plt.show()
