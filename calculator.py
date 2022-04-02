import math

import numpy as np

# Variables#
length = 5
height = 2.5
width = 4


###########

# x - distance from left wall to receiver
def wall_once_reflected_path_length_and_angle(x):
    if x < width / 2:
        x = -x + width
    a2_side = ((length-0.5)*width/2)/(x+width/2)
    a1_side = length-0.5-a2_side
    c1_side = math.sqrt(a1_side**2 + x**2)
    c2_side = math.sqrt(a2_side**2 + (width/2)**2)

    path = c1_side + c2_side
    angle = math.degrees(math.asin(x/c1_side))

    return path, angle

def ceiling_once_reflected_path_length_and_angle(x):
    los = los_length(x)
    c_side = math.sqrt(height+(los/2)**2)
    path = math.sqrt(5**2+los**2)
    angle = math.degrees(math.asin(height*2/path))

    return path, angle

# x - distance from left wall to receiver
def los_length(x):
    if x > width / 2:
        x = -x + width
    los = math.sqrt((width / 2 - x) ** 2 + (length-0.5) ** 2)

    return los


x = np.linspace(0.0, 4.0, 200)

for i in range(x.size):
    print('x='+str(x[i]))
    print('LOS_path ' + str(los_length(x[i])))
    print('Reflected path from wall ' + str(wall_once_reflected_path_length_and_angle(x[i])))
    print('Reflected path from ceiling ' + str(ceiling_once_reflected_path_length_and_angle(x[i])) + "\n")



