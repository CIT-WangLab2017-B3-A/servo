#!/usr/bin/python
# coding:UTF-8
# make_angle.py

import math

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
    print make_angle(90,-90+(36*5),20)
