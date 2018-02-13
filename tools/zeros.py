## model: Futaba RS304MD
## Temprate of move program

# import Library
import time, sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from uart import uart

# main program
def main():    
    # torque ON
    servo = uart()
    servo.ZeroAll()
    servo.Close()


if __name__ == '__main__':
    main()
