#SingleMotorTest.py
# test code that ramps each motor individually form 0-100-0 then changes direction and does it again then steps onto next motor.
import PicoRobotics
import utime


board = PicoRobotics.KitronikPicoRobotics()
directions = ["f","r"]

while True:
    
    for motor in range(4):
        for direction in directions:
            for speed in range(100):
                board.motorOn(motor+1, direction, speed)
                utime.sleep_ms(10) #ramp speed over 10x100ms => approx 1 second.
            for speed in range(100):
                board.motorOn(motor+1, direction, 100-speed) #ramp down
                utime.sleep_ms(10) #ramp speed over 10x100ms => approx 1 second.
        utime.sleep_ms(500)#pause between motors 
    
