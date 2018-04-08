'''
model: Futaba RS304MD
Temprate of move program
'''
# import Library
import sys
import os
import time
from uart import uart
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

# example
def Tester(servo, ID, Angle):
    # Speed
    Speed = 0.01
    Flag = 0x00
    print('press ctrl+c to quit')
    try:
        Data = servo.Angle_Speed(Angle, Speed)
        TxData = servo.ShortPacket(ID, Flag, servo.ADDRESS_POSITION, 0x01, Data)
        servo.Write(TxData)
    except:
        servo.Close()

argv = iter(sys.argv)
servo = uart()

# loop of argument
next(argv)
for ID in argv:
    # Torque ON
    servo.Torque(ID, servo.ON)
    servo.Tester(int(ID), 30)
    # wait
    time.sleep(1.0)

    servo.Tester(int(ID), 0)
    # wait
    time.sleep(1.0)
    # Torque OFF
    servo.Torque(ID, servo.OFF)
servo.Close()