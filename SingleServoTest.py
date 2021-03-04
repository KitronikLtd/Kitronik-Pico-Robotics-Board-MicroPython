#SingleServoTest.py
# test code that ramps each servo individually from 0-180-0 
import robotics
import utime


board = robotics.KitronikPicoRobotics()
while True:
   
    for servo in range(8):
        for degrees in range(180):
            board.servoWrite(servo+1, degrees)
            utime.sleep_ms(10) #ramp speed over 10x180ms => approx 2 seconds.
        for degrees in range(180):
            board.servoWrite(servo+1, 180-degrees)
            utime.sleep_ms(10) #ramp speed over 10x180ms => approx 2 seconds.
        board.servoWrite(servo+1, 90)
        utime.sleep_ms(50)#pause between servos 
