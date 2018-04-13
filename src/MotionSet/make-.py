#!/usr/bin/python
#coding: utf-8

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
                __Yop = 1 if self.__LegNumber[i]%2 else -1 # [1 or -1]
                __Yoff = self.__offset_y if (self.__LegNumber[i]==2) or (self.__LegNumber[i]==3) else 0
                __change_xyz = change_coodinate((__y[i]-__Yoff)*__Yop, __x[i], __z[i], self.__ChangeAngle[self.__LegNumber[i]])
                __AngleData = make_angle(__change_xyz[0], __change_xyz[1], __change_xyz[2])

                if (__LegPerSpeed*j)+i==len(self.__LegNumber)-1:
                    __csvWrite.writerow(DataOut(self.__LegNumber[i], __Speed[j] if not lenSpeed==1 else __Speed, __AngleData))
                else:
                    __csvWrite.writerow(DataOut(self.__LegNumber[i], __Speed[j] if not lenSpeed==1 else __Speed, __AngleData, '&'))
        __fp.close()

if __name__ == "__main__":
    SpeedHigh = 0.0
    SpeedLow  = 0.15
    y=120
#   <   > = parameter([脚no.],出力ファイル名)
    StandAll = parameter([0,3,4,1,2,5], '/home/pi/Program/servo/parameter/StandAll.csv')
    Ahead0 = parameter([0,3,4], '/home/pi/Program/servo/parameter/Ahead/Ahead0.csv')
    DownRight = parameter([0,3,4], '/home/pi/Program/servo/parameter/Ahead/DownRight.csv')
    PullRight = parameter([0,3,4,1,2,5], '/home/pi/Program/servo/parameter/Ahead/PullRight.csv')
    DownLeft = parameter([1,2,5], '/home/pi/Program/servo/parameter/Ahead/DownLeft.csv')
    PullLeft = parameter([1,2,5,0,3,4], '/home/pi/Program/servo/parameter/Ahead/PullLeft.csv')

#   <   >.make(Speed array, Position Matrix(x,y,z))
    Position = [
        [0, y, -30],
        [0, y, -30],
        [0, y, -30],
        [0, y, -30],
        [0, y, -30],
        [0, y, -30]
    ]
    StandAll.make(SpeedHigh, Position)

    Position = [
        [70*math.sin(math.radians(90)), y, 0],
        [70*math.sin(math.radians(90)), y, 0],
        [70*math.cos(math.radians(90)), y, 0]
    ]
    Ahead0.make(SpeedHigh, Position)

    Position = [
        [70*math.sin(math.radians(90)), y, -50],
        [70*math.sin(math.radians(90)), y, -50],
        [70*math.cos(math.radians(90)), y, -50]
    ]
    DownRight.make(SpeedHigh, Position)

    Position = [
        [70*math.sin(math.radians(0)), y, -50],
        [70*math.sin(math.radians(0)), y, -50],
        [-70*math.cos(math.radians(0)), y, -50],
        [70*math.sin(math.radians(90)), y, -20],
        [70*math.sin(math.radians(90)), y, -20],
        [70*math.cos(math.radians(90)), y, -20]
    ]
    PullRight.make([SpeedLow, SpeedHigh], Position)

    Position = [
        [70*math.sin(math.radians(90)), y, -50],
        [70*math.sin(math.radians(90)), y, -50],
        [70*math.cos(math.radians(90)), y, -50]
    ]
    DownLeft.make(SpeedHigh, Position)

    Position = [
        [70*math.sin(math.radians(0)), y, -50],
        [70*math.sin(math.radians(0)), y, -50],
        [-70*math.cos(math.radians(0)), y, -50],
        [70*math.sin(math.radians(90)), y, -20],
        [70*math.sin(math.radians(90)), y, -20],
        [70*math.cos(math.radians(90)), y, -20]
    ]
    PullLeft.make([SpeedLow, SpeedHigh], Position)
