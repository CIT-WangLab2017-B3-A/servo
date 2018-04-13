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
        __csvWrite = csv.writer(__fp)

        for j in xrange(lenSpeed):
            for i in xrange(__LegPerSpeed):
                k = __LegPerSpeed * j + i
                __Yop = 1 if self.__LegNumber[k]%2 else -1 # [1 or -1]
                __Yoff = self.__offset_y if (self.__LegNumber[k]==2) or (self.__LegNumber[k]==3) else 0
                __change_xyz = change_coodinate((__y[k]-__Yoff)*__Yop, __x[k], __z[k], self.__ChangeAngle[self.__LegNumber[k]])
                __AngleData = make_angle(__change_xyz[0], __change_xyz[1], __change_xyz[2])

                if k == len(self.__LegNumber)-1:
                    __csvWrite.writerow(DataOut(self.__LegNumber[k], __Speed[j] if not lenSpeed==1 else __Speed, __AngleData))
                else:
                    __csvWrite.writerow(DataOut(self.__LegNumber[k], __Speed[j] if not lenSpeed==1 else __Speed, __AngleData, '&'))
        __fp.close()

if __name__ == "__main__":
    SpeedHigh = 0.1
    SpeedLow  = 0.25
#   <   > = parameter([脚no.],出力ファイル名)
    PATH='/home/pi/Program/servo/parameter/'
    StandAll = parameter([0,3,4,1,2,5], PATH+'StandAll.csv')
    Ahead0 = parameter([0,3,4], PATH+'Ahead/Ahead0.csv')
    DownRight = parameter([0,3,4], PATH+'Ahead/DownRight.csv')
    PullRight = parameter([0,3,4,1,2,5], PATH+'Ahead/PullRight.csv')
    DownLeft = parameter([1,2,5], PATH+'Ahead/DownLeft.csv')
    PullLeft = parameter([1,2,5,0,3,4], PATH+'Ahead/PullLeft.csv')

    x = 0
    y0 = 80
    z0 = -80
#   <   >.make(Speed array, Position Matrix(x,y,z))
    Position = [
        [x, y0, z0],
        [x, y0, z0],
        [x, y0, z0],
        [x, y0, z0],
        [x, y0, z0],
        [x, y0, z0]
    ]
    StandAll.make(SpeedHigh, Position)
    print "StandAll: OK"

    Position = [
        [x, 40+y0, z0+5],
        [x, -40+y0, z0+5],
        [x, 40+y0, z0+5]
    ]
    Ahead0.make(SpeedHigh, Position)
    print "Ahead0: OK"

    Position = [
        [x, 40+y0, z0-10],
        [x, -40+y0,z0-10],
        [x, 40+y0, z0-10]
    ]
    DownRight.make(SpeedHigh, Position)
    print "DownRight: OK"

    Position = [
        [x, y0, z0-10],
        [x, y0, z0-10],
        [x, y0, z0-10],
        [x, -40+y0, z0+5],
        [x, 40+y0, z0+5],
        [x, -40+y0, z0+5]
    ]
    PullRight.make([SpeedLow, SpeedHigh], Position)
    print "PullRight: OK"

    Position = [
        [x, -40+y0, z0-10],
        [x, 40+y0, z0-10],
        [x, -40+y0, z0-10]
    ]
    DownLeft.make(SpeedHigh, Position)
    print "DownLeft: OK"

    Position = [
        [x, y0, z0-10],
        [x, y0, z0-10],
        [x, y0, z0-10],
        [x, 40+y0, z0+5],
        [x, -40+y0, z0+5],
        [x, 40+y0, z0+5]
    ]
    PullLeft.make([SpeedLow, SpeedHigh], Position)
    print "PullLeft: OK"
