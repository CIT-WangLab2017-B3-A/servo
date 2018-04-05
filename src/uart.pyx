#!/usr/bin/python
# coding: utf-8

# urat module made of Hiroki Yumigeta
import sys
import serial
import time
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
        self.ADDRESS_POSITION = 0x1E # position's address
        self.ADDRESS_TORQUE   = 0x24

        # open port
        self.uart = serial.Serial(port, rate)

    # サーボにデータを送信する
    def Write(self, TxData):
        self.uart.write(TxData)

    # 角度と速度をデータフォーマットどおりに変換
    def Angle_Speed(self, fAngle, fSpeed):
        Angle = int(10.0 *float(fAngle))
        Speed = int(100.0*float(fSpeed))
        tmpData = [Angle, (Angle>>8), Speed, (Speed>>8)]
        Data = map(lambda x:x&0x00FF, tmpData)
        return Data

    # Check-Sumの計算
    def CheckSum(self, Data):
        check=0x00
        for x in Data:
            check ^= x
        return check

    # Short Packet
    def ShortPacket(self, ID, Flag, Address, Cnt, Data):
        # packet header
        TxData = [0xFA, 0xAF]
        if type(Data)==type([]): # array
            Length = len(Data)
            tmpData = [ID, Flag, Address, Length, Cnt]
            tmpData.extend(Data)
        elif type(Data)==type(None):# None data(ex.reboot)
            tmpData = [ID, Flag, Address, 0x00, Cnt]
        else: # not array
            Length = 0x01
            tmpData = [ID, Flag, Address, Length, Cnt]
            tmpData.append(Data)
        # CheckSum
        tmpData.append(self.CheckSum(tmpData))
        TxData.extend(tmpData)
        return TxData

    # Long Packet
    def LongPacket(self, Address, Data):
        # packet header
        TxData = [0xFA, 0xAF]
        Length = len(Data[0])# data par servo
        Cnt = len(Data)# servos
        tmpData = [0x00, 0x00, Address, Length, Cnt]
        for x in Data:
            tmpData.extend(x)
        # checkSum
        tmpData.append(self.CheckSum(tmpData))
        TxData.extend(tmpData)
        return TxData

    # Control func
    # 再起動
    def Reboot(self, ID=self.ALLSERVOS):
        TxData = self.ShortPacket(ID, 0x20, self.ALLSERVOS, 0x00, None)
        self.Write(TxData)
        print('Reboot:Finish!')

    # ROMに書き込む
    def RomWrite(self, ID=self.ALLSERVOS):
        TxData = self.ShortPacket(ID, 0x40, 0xFF, 0x00, None)
        self.Write(TxData)
        print('Write ROM:Finish!')
    
    # サーボのID変更
    def ChangeID(self, NewID, ID=self.ALLSERVOS):
        TxData = self.ShortPacket(ID, 0x00, self.ADDRESS_ID, 0x01, NewID)
        self.Write(TxData)
        self.RomWrite(NewID)
        self.Reboot(NewID)
        print('Change ID:Finish!')

    # サーボの回転方向の反転
    def Reverse(self, ID, SW):
        TxData = self.ShortPacket(ID, 0x00, self.ADDRESS_REVERSE, 0x01, SW)
        self.Write(TxData)
        self.RomWrite(ID)
        self.Reboot(ID)
        print('Reverse Rotate:Finish!')

    # トルク制御関数
    def Torque(self, ID, SW):
        TxData = self.ShortPacket(ID, 0x00, self.ADDRESS_TORQUE, 0x01, SW)
        self.Write(TxData)

    # サーボのトルクを発生させる
    def Start(self):
        self.Torque(self.ALLSERVOS, self.ON)

    # サーボをスタンバイモードにする
    def Stop(self):
        self.Torque(self.ALLSERVOS, self.PANTCH)

    # 全てのサーボを初期位置に戻す
    def ZeroAll(self):
        Data = self.Angle_Speed(0, 0.01)
        self.Torque(self.ALLSERVOS, self.ON)
        TxData = self.ShortPacket(self.ALLSERVOS, 0x00, self.ADDRESS_POSITION, 0x01, Data)
        self.Write(TxData)
        time.sleep(2.0)
        self.Stop()

    # testProgram
    def Tester(self, ID):
        self.Torque(ID, self.ON)
        for j in xrange(2):#two loop
            Data = self.Angle_Speed(30, 0.01)
            TxData = self.ShortPacket(ID, 0x00, self.ADDRESS_POSITION, 0x01, Data)
            self.Write(TxData)
            time.sleep(1.0)
            Data = self.Angle_Speed(0, 0.01)
            TxData = self.ShortPacket(ID, 0x00, self.ADDRESS_POSITION, 0x01, Data)
            self.Write(TxData)
            time.sleep(1.0)
        self.Torque(ID, self.OFF)

    # サーボを落とす
    def Close(self):
        self.Torque(self.ALLSERVOS, self.OFF)

    # デストラクタ
    def __del__(self):
        self.uart.close()
