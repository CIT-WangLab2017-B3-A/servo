#!/usr/bin/python
# coding: utf-8

# sample program

# import Library
import sys
sys.path.append('src')
import time
import numpy as np
from move import move

# main program
def main():
    # nomal array
    Data=[\
        [[0],[20.0,0.1],[20.0,0.1],[20.0,0.1]],\
        [[3],[20.0,0.1],[20.0,0.1],[20.0,0.1]],\
        [[4],[20.0,0.1],[20.0,0.1],[20.0,0.1]],\
    ]

    # numpy array
    npData=np.array([\
        [[1],[20.0,0.1],[20.0,0.1],[20.0,0.1]],\
        [[2],[20.0,0.1],[20.0,0.1],[20.0,0.1]],\
        [[5],[20.0,0.1],[20.0,0.1],[20.0,0.1]],\
    ])

    # class move(LEG_SERVOS=3, port='/dev/ttyS0', rate=115200)
    servo = move()
    try:
        # 従来型(file)
        servo.Action('zero.csv',1.0)
        # 配列(普通の)
        print Data
        servo.Action(Data)
        # 配列(numpy)
        servo.Action(npData)
    except KeyboardInterrupt:
        servo.Close()
    time.sleep(1.0)
    servo.Close()

if __name__ == '__main__':
    main()
