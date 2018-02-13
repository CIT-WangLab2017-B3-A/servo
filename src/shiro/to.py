#!/usr/bin/python
# coding:UTF-8
# make_angle.py

import math

def change_coodinate(x,y,z,theta):
    "change coodinate"  # x[mm],y[mm],z[mm],theta[deg]
    theta = math.radians(theta)
    print "theta",theta
    cx = (x * math.cos(theta)) + (y * math.sin(theta))
    cy = -(x * math.sin(theta)) + (y * math.cos(theta))
    cz = z
    return map(lambda n: round(n, 6),[cx,cy,cz])

def make_angle(x, y, z):
    "Calculation theta's deg"    # x[mm],y[mm],z[mm]
    length1 = 30    #[mm]
    length2 = 55    #[mm]
    length3 = 80    #[mm]

    alpha = math.sqrt((x*x)+(y*y)) - length1
    check_value = (
        pow(pow(alpha,2) + pow(z,2) + pow(length2,2)
        + pow(length3,2),2) - (2 * ( pow( pow(alpha,2) + pow(z,2),2) + pow(length2,4) + pow(length3,4)))
    )
    if check_value > 0:
        k = math.sqrt(
            check_value
        )
    else:
        return None
    theta1 = math.atan2(y,x)
    theta2 = math.atan2(z,alpha) + math.atan2(k, (alpha*alpha) + (z*z) + (length2*2) - (length3*2))
    theta3 = -math.atan2(k, (alpha*alpha) + (z*z) - pow(length2,2) - pow(length3,2))
    theta = map(lambda n: math.degrees(n), [theta1, -theta2, -theta3])
    return theta    #[deg]

if __name__ == "__main__":
    init_xyz = [90, 0, 20]
    print init_xyz
    change_xyz = change_coodinate(init_xyz[0], init_xyz[1], init_xyz[2], 30)
    print change_xyz
    print make_angle(change_xyz[0],change_xyz[1],change_xyz[2])
