#!/usr/bin/python
# coding: utf-8
__author__ = 'Hiroki Yumigeta'
#import sys
import time
import serial
class uart(object):
    def __init__(self, port='/dev/ttyS0', rate=115200):
        # all servos
        self.ALLSERVOS = 0xFF

        # torque mode
        self.OFF    = 0x00
        self.ON     = 0x01
        self.PANTCH = 0x02

        # address
        self.ADDRESS_ID       = 0x04
        self.ADDRESS_REVERSE  = 0x05
        self.ADDRESS_POSITION = 0x1E
        self.ADDRESS_TORQUE   = 0x24

        # Flag
        self.FLAG_REBOOT    = 0x20
        self.FLAG_WRITE_ROM = 0x40

        # open port
        self.uart = serial.Serial(port, rate)

    # サーボにデータを送信する
    def Write(self, TxData):
        self.uart.write(TxData)

    # 角度と速度をデータフォーマットどおりに変換
    def Angle_Speed(self, fAngle, fSpeed):
        Angle   = int(10.0 *float(fAngle))
        Speed   = int(100.0*float(fSpeed))
        tmpData = [Angle, (Angle>>8), Speed, (Speed>>8)]
        Data    = map(lambda x:x&0x00FF, tmpData)
        return Data

    # CheckSumの計算
    def CheckSum(self, Data):
        check = 0x00
        for x in Data:
            check ^= x
        return check

    # Short Packet
    def ShortPacket(self, ID, Flag, Address, Cnt, Data):
        TxData = [0xFA, 0xAF]# packet header
        # array
        if type(Data)==type([]):
            Length  = len(Data)
            tmpData = [ID, Flag, Address, Length, Cnt]
            tmpData.extend(Data)
        # None data(ex.reboot)
        elif type(Data)==type(None):
            tmpData = [ID, Flag, Address, 0x00, Cnt]
        # not array
        else:
            Length  = 0x01
            tmpData = [ID, Flag, Address, Length, Cnt]
            tmpData.append(Data)
        # CheckSum
        tmpData.append(self.CheckSum(tmpData))
        TxData.extend(tmpData)
        return TxData

    # Long Packet
    def LongPacket(self, Address, Data):
        ID=Flag=0x00
        TxData  = [0xFA, 0xAF]# packet header
        Length  = len(Data[0])# サーボ1個当たりのバイト数
        Cnt     = len(Data)# サーボ数
        tmpData = [ID, Flag, Address, Length, Cnt]
        for x in Data:
            tmpData.extend(x)
        # CheckSum
        tmpData.append(self.CheckSum(tmpData))
        TxData.extend(tmpData)
        return TxData

    # 再起動
    def Reboot(self, ID):
        Length  = 0x00
        Address = 0xFF
        TxData  = self.ShortPacket(ID, self.FLAG_REBOOT, Address, Length, None)
        self.Write(TxData)
        print('Reboot:Finish!')

    # ROMに書き込む
    def RomWrite(self, ID):
        Length  = 0x00
        Address = 0xFF
        TxData  = self.ShortPacket(ID, self.FLAG_WRITE_ROM, Address, Length, None)
        self.Write(TxData)
        print('Write ROM:Finish!')
    
    # サーボのID変更
    def ChangeID(self, NewID, ID):
        Flag   = 0x00
        TxData = self.ShortPacket(ID, Flag, self.ADDRESS_ID, 0x01, NewID)
        self.Write(TxData)
        self.RomWrite(NewID)
        self.Reboot(NewID)
        print('Change ID:Finish!')

    # サーボの回転方向の反転
    def Reverse(self, ID, SW):
        Flag   = 0x00
        TxData = self.ShortPacket(ID, Flag, self.ADDRESS_REVERSE, 0x01, SW)
        self.Write(TxData)
        self.RomWrite(ID)
        self.Reboot(ID)
        print('Reverse Rotate:Finish!')

    # トルク制御関数
    def Torque(self, ID, SW):
        Flag   = 0x00
        TxData = self.ShortPacket(ID, Flag, self.ADDRESS_TORQUE, 0x01, SW)
        self.Write(TxData)

    # サーボのトルクを発生させる
    def Start(self):
        self.Torque(self.ALLSERVOS, self.ON)

    # サーボをスタンバイモードにする
    def Stop(self):
        self.Torque(self.ALLSERVOS, self.PANTCH)

    # 全てのサーボを初期位置に戻す
    def ZeroAll(self):
        Flag = 0x00
        Data = self.Angle_Speed(0, 0.01)
        self.Torque(self.ALLSERVOS, self.ON)
        TxData = self.ShortPacket(self.ALLSERVOS, Flag, self.ADDRESS_POSITION, 0x01, Data)
        self.Write(TxData)
        time.sleep(2.0)
        self.Stop()

    # サーボを落とす
    def Close(self):
        self.Torque(self.ALLSERVOS, self.OFF)

    # デストラクタ
    def __del__(self):
        self.uart.close()