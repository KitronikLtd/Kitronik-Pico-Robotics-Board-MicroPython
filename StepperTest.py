import robotics
import utime

board = robotics.KitronikPicoRobotics()
directions = ["f","r"]

while True:
        for direction in directions:
             for stepcount in range(200):
                board.step(1,direction,8)
                board.step(2,direction,8)
        utime.sleep_ms(500)#pause between motors 
    
    