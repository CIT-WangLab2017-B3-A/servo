#!/usr/bin/python
#coding: utf-8

# グリップ有り無しでの滑り具合の検証(重し有り無し含む)

import numpy as np
import csv
from inverse import *
class parameter:
    __offset_y = 20
    __ChangeAngle = [120,60,-180,0,-120,-60]
    def __init__(self, LegNumber, FILENAME):
        self.__FILENAME = FILENAME
        self.__LegNumber = LegNumber

    def make(self, Speed, Position):
        lenSpeed = len(Speed) if isinstance(Speed, list) else 1
        if len(self.__LegNumber)%lenSpeed:
            print "Value Error"
            exit()
        __Speed = Speed
        
        __LegPerSpeed = len(self.__LegNumber)/lenSpeed

        __Posmat=np.matrix(Position)
        __x = __Posmat[:,0]
        __y = __Posmat[:,1]
        __z = __Posmat[:,2]
        __fp = open(self.__FILENAME,'w')
        __csvWrite = csv.writer(__fp, lineterminator='\n')

        for j in xrange(lenSpeed):
            for i in xrange(__LegPerSpeed):
                k = __LegPerSpeed * j + i
                __Yop = 1 if self.__LegNumber[k]%2 else -1 # [1 or -1]
                __Yoff = self.__offset_y if (self.__LegNumber[k]==2) or (self.__LegNumber[k]==3) else 0
                __change_xyz = change_coodinate((__y[k]-__Yoff)*__Yop, __x[k], __z[k], self.__ChangeAngle[self.__LegNumber[k]])
                __AngleData = make_angle(__change_xyz[0], __change_xyz[1], __change_xyz[2])
                if k==len(self.__LegNumber)-1:
                    __csvWrite.writerow(DataOut(self.__LegNumber[k], __Speed[j] if not lenSpeed==1 else __Speed, __AngleData))
                else:
                    __csvWrite.writerow(DataOut(self.__LegNumber[k], __Speed[j] if not lenSpeed==1 else __Speed, __AngleData, '&'))
        __fp.close()

if __name__ == "__main__":
    SpeedHigh = 0.0
    SpeedLow  = 0.05
    x     = 120
    y     = 120
    z0    = -50
    Zup   = 5
    Zdown = -10
    theta_1 = math.radians(0)
    theta_2 = math.radians(0)
    theta_3 = math.radians(-45)
#   <   > = parameter([脚no.],出力ファイル名)
    PATH = '/home/pi/Program/servo/parameter/'
    StandAll = parameter([0,3,4,1,2,5], PATH+'StandAll.csv')
    Ahead0 = parameter([0,3,4], PATH+'Ahead/Ahead0.csv')
    DownRight = parameter([0,3,4], PATH+'Ahead/DownRight.csv')
    PullRight = parameter([0,3,4,1,2,5], PATH+'Ahead/PullRight.csv')
    DownLeft = parameter([1,2,5], PATH+'Ahead/DownLeft.csv')
    PullLeft = parameter([1,2,5,0,3,4], PATH+'Ahead/PullLeft.csv')

#   <   >.make(Speed array, Position Matrix(x,y,z))
    Position = [
        [x*math.sin(theta_1), y*math.cos(theta_1), z0],
        [x*math.sin(theta_2), y*math.cos(theta_2)-30, z0],
        [x*math.sin(theta_3), y*math.cos(theta_3), z0],

        [x*math.sin(theta_1), y*math.cos(theta_1), z0],
        [x*math.sin(theta_2), y*math.cos(theta_2)-30, z0],
        [x*math.sin(theta_3), y*math.cos(theta_3), z0]
    ]
    StandAll.make(SpeedHigh, Position)

    Position = [
        [x*math.sin(theta_1)+70, y*math.cos(theta_1), z0+Zup],
        [x*math.sin(theta_2)+70, y*math.cos(theta_2)-30, z0+Zup],
        [x*math.sin(theta_3)+70, y*math.cos(theta_3), z0+Zup]
    ]
    Ahead0.make(SpeedHigh, Position)

    Position = [
        [x*math.sin(theta_1)+70, y*math.cos(theta_1), z0+Zdown],
        [x*math.sin(theta_2)+70, y*math.cos(theta_2)-30, z0+Zdown],
        [x*math.sin(theta_3)+70, y*math.cos(theta_3), z0+Zdown]
    ]
    DownRight.make(SpeedHigh, Position)

    Position = [
        [x*math.sin(theta_1), y*math.cos(theta_1), z0+Zdown],
        [x*math.sin(theta_2), y*math.cos(theta_2)-30, z0+Zdown],
        [x*math.sin(theta_3), y*math.cos(theta_3), z0+Zdown],

        [x*math.sin(theta_1)+70, y*math.cos(theta_1), z0+Zup],
        [x*math.sin(theta_2)+70, y*math.cos(theta_2)-30, z0+Zup],
        [x*math.sin(theta_3)+70, y*math.cos(theta_3), z0+Zup]
    ]
    PullRight.make([SpeedLow, SpeedHigh], Position)

    Position = [
        [x*math.sin(theta_1)+70, y*math.cos(theta_1), z0+Zdown],
        [x*math.sin(theta_2)+70, y*math.cos(theta_2)-30, z0+Zdown],
        [x*math.sin(theta_3)+70, y*math.cos(theta_3), z0+Zdown],
    ]
    DownLeft.make(SpeedHigh, Position)

    Position = [
        [x*math.sin(theta_1), y*math.cos(theta_1), z0+Zdown],
        [x*math.sin(theta_2), y*math.cos(theta_2)-30, z0+Zdown],
        [x*math.sin(theta_3), y*math.cos(theta_3), z0+Zdown],

        [x*math.sin(theta_1)+70, y*math.cos(theta_1), z0+Zup],
        [x*math.sin(theta_2)+70, y*math.cos(theta_2)-30, z0+Zup],
        [x*math.sin(theta_3)+70, y*math.cos(theta_3), z0+Zup],
    ]
    PullLeft.make([SpeedLow, SpeedHigh], Position)
