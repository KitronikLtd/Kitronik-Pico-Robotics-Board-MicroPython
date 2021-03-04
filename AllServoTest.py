#AllServoTest.py
# test code that ramps each servo from 0-180-0 
import robotics
import utime


board = robotics.KitronikPicoRobotics()
while True:
    for degrees in range(180):
        for servo in range(1,9):
            board.servoWrite(servo, degrees)
        utime.sleep_ms(10) #ramp speed over 10x180ms => approx 2 seconds.
    for degrees in range(180):
        for servo in range(1,9):
            board.servoWrite(servo, 180-degrees)
        utime.sleep_ms(10) #ramp speed over 10x180ms => approx 2 seconds.
