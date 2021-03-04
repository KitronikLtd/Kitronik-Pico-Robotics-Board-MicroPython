#AllMotorTest.py
# test code that ramps each motor 0-100-0 then changes direction and does it again.
#all motors run at once, but with staggered timings

import robotics
import utime


board = robotics.KitronikPicoRobotics()
directions = ["f","r"]

while True:
    for direction in directions:
        for speed in range(0,25):
            board.motorOn(1, direction, speed)
            board.motorOn(2, direction, 25-speed)
            board.motorOn(3, direction, 50-speed)
            board.motorOn(4, direction, 75-speed)
            utime.sleep_ms(100) #ramp speed over 25x100ms => approx 2.5 second.
        for speed in range(0,25):
            board.motorOn(1, direction, 25+speed)
            board.motorOn(2, direction, speed)
            board.motorOn(3, direction, 25-speed)
            board.motorOn(4, direction, 50-speed)
            utime.sleep_ms(100) 
        for speed in range(0,25):
            board.motorOn(1, direction, 50+speed)
            board.motorOn(2, direction, 25+speed)
            board.motorOn(3, direction, speed)
            board.motorOn(4, direction, 25-speed)
            utime.sleep_ms(100) 
        for speed in range(0,25):
            board.motorOn(1, direction, 75+speed)
            board.motorOn(2, direction, 50+speed)
            board.motorOn(3, direction, 25+speed)
            board.motorOn(4, direction, speed)
            utime.sleep_ms(100) 
        for speed in range(0,25):
            board.motorOn(1, direction, 100-speed)
            board.motorOn(2, direction, 75+speed)
            board.motorOn(3, direction, 50+speed)
            board.motorOn(4, direction, 25+speed)
            utime.sleep_ms(100) 
        for speed in range(0,25):
            board.motorOn(1, direction, 75-speed)
            board.motorOn(2, direction, 100-speed)
            board.motorOn(3, direction, 75+speed)
            board.motorOn(4, direction, 50+speed)
            utime.sleep_ms(100)
        for speed in range(0,25):
            board.motorOn(1, direction, 50-speed)
            board.motorOn(2, direction, 75-speed)
            board.motorOn(3, direction, 100-speed)
            board.motorOn(4, direction, 75+speed)
            utime.sleep_ms(100) 
        for speed in range(0,25):
            board.motorOn(1, direction, 25-speed)
            board.motorOn(2, direction, 50-speed)
            board.motorOn(3, direction, 75-speed)
            board.motorOn(4, direction, 100-speed)
            utime.sleep_ms(100) 

  
    
