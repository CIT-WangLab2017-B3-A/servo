#!/usr/bin/python
# coding: utf-8

#import Library
import serial
import time
import sys

#variable
args = sys.argv

#setup Baudrate
servo = serial.Serial('/dev/ttyS0', 115200, timeout=5)

# torque ON
def Res(ID):
    check = 0x00
    TxData = [0xFA, 0xAF, ID, 0x0F, 0x0A, 0x01, 0x00, check]
    #RxData = []*15
    for i in range(2, 7):
        check = check^TxData[i]
    TxData[7] = check
    servo.write(TxData)
    time.sleep(0.5)
    #for i in range(10):
    RxData = servo.read(1)
    #RxData = RxData.split(' ')
    #time.sleep(1)
    print (RxData)
    time.sleep(0.00025)

Res(0x03)
time.sleep(0.5)
servo.close()
print 'Done\n'

