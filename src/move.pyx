#!/usr/bin/python
# coding: utf-8
__author__ = 'Hiroki Yumigeta'

#import sys
#import os.path
import time
import numpy as np
#import serial
from uart import *
class move(uart):
    def __init__(self, LEG_SERVOS=3, port='/dev/ttyS0', rate=115200):
        super(move, self).__init__(port, rate)
        self.LegServos = LEG_SERVOS
        self.Torque(0xFF, self.ON)

    # CSVファイルのimport
    def FileImport(self):
        Data = []
        while True:
            try:
                line = self.it.next()# 1行ずつ読み取る
            except StopIteration:
                return None
            DataList = line[:-1].split(',')# 配列化
            # DataListの処理
            Group  = int(DataList[0])# Group
            fSpeed = DataList[1]# Speed
            for i in xrange(self.LegServos):
                VID     = (3*Group) + (i+1)# ID
                fAngle  = DataList[i+2]# 角度
                CtrData = self.Angle_Speed(fAngle, fSpeed)# float to int
                CtrData.insert(0, VID)
                Data.append(CtrData)# 2d array
            if DataList[-1] != ('&' or '&'+'\r'):# 配列の最後
                break
        return Data

    # 引数がファイル名のとき
    def CSVAct(self, FileName, sleep):
        try:
            # CSVファイルのopen
            self.fp = open('parameter/'+FileName,'r')
            self.it = iter(self.fp.readline,'')# イテレータ
            # データの読み取り
            Data = self.FileImport()
            while Data != None:
                self.Write(self.LongPacket(self.ADDRESS_POSITION, Data))
                time.sleep(sleep)
                Data = self.FileImport()
            # CSVファイルのclose
            self.fp.close()
        except IOError:
            print('File is not found')

    # 引数がlistのとき
    def ListAct(self, Data):
        CtrData = []
        #sleepTime = 0.0
        for Datalist in Data:
            #[[ID],[A1,S1][A2,S2][A3,S3]]
            Group = Datalist.pop(0)# Group
            #[[A1,S1][A2,S2][A3,S3]]
            for i in range(len(Datalist)):
                VID     = (3*int(Group[0])) + (i+1)# ID
                tmpData = self.Angle_Speed(Datalist[i][0], Datalist[i][1])
                tmpData.insert(0, VID)
                CtrData.append(tmpData)
                #sleepTime += Datalist[i][1] 違う気がする(上も修正)
                sleepTime = max(sleepTime, Datalist[i][1])
        self.Write(self.LongPacket(self.ADDRESS_POSITION, CtrData))
        time.sleep(sleepTime)

    # 引数による処理の振分け
    def Action(self, InData, sleep=1.0):
        try:
            # NumPy
            CnvData = InData.tolist()
            self.ListAct(CnvData)
        except AttributeError:
            # list
            if type(InData)==type([]):
                self.ListAct(InData)
            # CSV
            elif type(InData)==type(''):
                self.CSVAct(InData, sleep)
            # Other
            else:
                print('Value Error(data is File or List)')