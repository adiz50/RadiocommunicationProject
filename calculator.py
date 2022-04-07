import cmath
import math

import numpy as np

# Variables#
length = 5
height = 2.5
width = 4
additional_room_length = 2
additional_room_width = 1.5
concrete = 5.31
light = 3e8
fc = 2.4e9
lam = light / fc


###########

# x - distance from left wall to receiver
def wall_once_reflected_path_length_and_angle(x):
    # if x < width / 2:
    #    x = -x + width
    a2_side = ((length - 0.5) * width / 2) / (x + width / 2)
    a1_side = length - 0.5 - a2_side
    c1_side = math.sqrt(a1_side ** 2 + x ** 2)
    c2_side = math.sqrt(a2_side ** 2 + (width / 2) ** 2)

    path = c1_side + c2_side
    if c1_side == 0:
        c1_side = 0.0000001

    angle = math.asin(x / c1_side)


    return path, angle


def reflectance(angle):
    a = (math.cos(angle) - math.sqrt(concrete - math.sin(angle) ** 2)) / (
            math.cos(angle) + math.sqrt(concrete - math.sin(angle) ** 2))
    return a


def ceiling_once_reflected_path_length_and_angle(x):
    los = los_length(x)
    path = math.sqrt((height * 2) ** 2 + los ** 2)
    angle = math.asin(height * 2 / path)

    return path, angle


# x - distance from left wall to receiver
def los_length(x):
    if x > width / 2:
        x = -x + width
    los = math.sqrt((width / 2 - x) ** 2 + (length - 0.5) ** 2)

    return los


def received_power_los(x):
    fi = -1 * (2 * math.pi * fc * los_length(x)) / light
    P = 10 * math.log10(abs((1 / los_length(x)) * cmath.exp(math.pi * fi * 1j)) ** 2)

    return P


def received_power_multipath1(x):
    path_los = los_length(x)
    path_wall, angles_wall = wall_once_reflected_path_length_and_angle(x)
    path_ceiling, angles_ceiling = ceiling_once_reflected_path_length_and_angle(x)

    fi1 = -1 * (2 * math.pi * fc * path_los) / light
    fi2 = -1 * (2 * math.pi * fc * path_wall) / light
    fi3 = -1 * (2 * math.pi * fc * path_ceiling) / light

    P1 = (1 / path_los) * cmath.exp(math.pi * fi1 * 1j)  # LOS
    P2 = (reflectance(angles_wall) / path_wall) * cmath.exp(math.pi * fi2 * 1j)  # Reflected path wall
    P3 = (reflectance(angles_ceiling) / path_ceiling) * cmath.exp(math.pi * fi3 * 1j)  # Reflected path ceiling
    sum = 10 * math.log10(abs(P1 + P2 + P3) ** 2)

    return sum


#x = np.linspace(0.0, 4.0, 200)

#for i in range(x.size):
#    print('x=' + str(x[i]))
#    print('LOS_path ' + str(los_length(x[i])))
#    print('Reflected path from wall ' + str(wall_once_reflected_path_length_and_angle(x[i])))
#    print('Reflected path from ceiling ' + str(ceiling_once_reflected_path_length_and_angle(x[i])) + "\n")
