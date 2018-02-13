#!/usr/bin/python
# coding:UTF-8
# make_angle.py
import math
import numpy as np

def change_coodinate(x,y,z,initTheta):
    "change coodinate"  # x[mm],y[mm],z[mm],initTheta[deg]
    initTheta = math.radians(initTheta)
    cosTheta = math.cos(initTheta)
    sinTheta = math.sin(initTheta)
    cx = (x * cosTheta) + (y * sinTheta)
    cy = -(x * sinTheta) + (y * cosTheta)
    cz = z
    return map(lambda n: round(n, 6), [cx,cy,cz])

def make_angle(x, y, z):
    "Calculation theta's deg"    # x[mm],y[mm],z[mm]
    theta_MAX = [80, 90, 135]
    length1 = 30    #[mm]
    length2 = 55    #[mm]
    length3 = 80    #[mm]
    pow_L = map(lambda n: pow(n, 2), [length1,length2,length3])
    pow2_L = map(lambda n: pow(n, 4), [length1,length2,length3])
    pow_xyz = map(lambda n: pow(n, 2), [x,y,z])
    alpha     = math.sqrt(pow_xyz[0]+pow_xyz[1]) - length1
    pow_alpha = pow(alpha,2)
    check_value = (
        pow(pow_alpha + pow_xyz[2] + pow_L[1] + pow_L[2] ,2)
        - (2*( pow( pow_alpha + pow_xyz[2] ,2) + pow2_L[1] + pow2_L[2]))
    )
    if check_value > 0:
        k = math.sqrt(check_value)
    else:
        print 'error: k is minus'
        return None
    theta1 = math.atan2(y,x)
    theta2 = (
        math.atan2(z,alpha)
        + math.atan2(k, pow_alpha + pow_xyz[2] + (length2*2) - (length3*2))
    )
    theta3 = -math.atan2(k, pow_alpha + pow_xyz[2] - pow_L[1] - pow_L[2])
    theta = map(lambda n: math.degrees(n), [theta1, -theta2, -theta3])
    if math.fabs(theta[0]) > theta_MAX[0]:
        print 'error: theta1 is out of range'
    if math.fabs(theta[1]) > theta_MAX[1]:
        print 'error: theta2 is out of range'
    if math.fabs(theta[2]) > theta_MAX[2]:
        print 'error: theta3 is out of range'
    return theta    #[deg]
def DataOut(group, Speed, Data, amp=None):
    dataline = [group, Speed]
    dataline.extend(np.round(Data))
    if amp == ('&' or '&\r'):
        dataline.extend('&')
    return dataline
