## model: Futaba RS304MD
## Temprate of move program

# import Library
import time, sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from uart import uart

# main program
def main():    
    args = sys.argv
    servo = uart()
    ID = int(args[1])
    rotate = args[2]
    if(rotate=='cw'):
        SW = 0x00
        servo.Inverse(ID,SW)
    elif(rotate=='ccw'):
        SW = 0x01
        servo.Inverse(ID,SW)
    servo.Close()

if __name__ == '__main__':
    main()
