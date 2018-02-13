#!/usr/bin/python
# coding: utf-8

# move module made of Hiroki Yumigeta
import numpy as np
import sys, os.path
import serial
import time
from uart import *
class move(uart):
    def __init__(self, LEG_SERVOS=3, port='/dev/ttyS0', rate=115200):
        super(move, self).__init__(port, rate)
        self.LegServos = LEG_SERVOS
        self.Torque(0xFF, self.ON)
    def FileOpen(self, FileName=None):
        try:
            self.fp = open(FileName,'r')
            self.it = iter(self.fp.readline,'')# イテレータ
        except:
            return IOError
    def FileClose(self):
        self.fp.close()
    def DataImport(self):
        Data = []
        while True:
            try:
                line = self.it.next()# 1行ずつ読み取る
            except StopIteration:
                return None
            DataList = line[:-1].split(',')# 配列化
            # DataListの処理
            Group  = DataList[0]# Group
            fSpeed = DataList[1]# Speed
            for i in xrange(self.LegServos):
                VID    = (3*int(Group)) + (i+1)# ID
                fAngle = DataList[i+2]# 角度
                # float to int
                CtrData = self.Angle_Speed(fAngle, fSpeed)
                CtrData.insert(0,VID)
                Data.append(CtrData)# 2d array
            if DataList[-1] != ('&' or '&'+'\r'):# 配列の最後
                break
        return Data
    def ListAct(self, Data):
        CtrData = []
        sleepTime = 0.0
        for Datalist in Data:
            #[[ID],[A1,S1][A2,S2][A3,S3]]
            Group = Datalist.pop(0)# Group
            #[[A1,S1][A2,S2][A3,S3]]
            for i in range(len(Datalist)):
                VID   = (3*int(Group[0])) + (i+1)# ID
                tmpData = self.Angle_Speed(Datalist[i][0], Datalist[i][1])
                tmpData.insert(0, VID)
                CtrData.append(tmpData)
                sleepTime += Datalist[i][1]
        self.Write(self.LongPacket(self.ADDRESS_POS, CtrData))
        time.sleep(sleepTime)
    def CSVAct(self, FileName, sleep):
        try:
            self.FileOpen('parameter/'+FileName)
            Data = self.DataImport()
            while Data != None:
                self.Write(self.LongPacket(self.ADDRESS_POS, Data))
                time.sleep(sleep)
                Data = self.DataImport()
            self.FileClose()
        except IOError:
            print 'File is not found'
    def Action(self, InData, sleep=1.0):
        try:
            CnvData=InData.tolist()
            self.ListAct(CnvData)
        except AttributeError:
            if type(InData)==type([]):
                self.ListAct(InData)
            elif type(InData)==type(''):
                self.CSVAct(InData,sleep)
            else:
                print 'Value Error(data is File or List)'
