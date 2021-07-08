import machine
import utime

class KitronikPicoRobotics:
    #Class variables - these should be the same for all instances of the class.
    # If you wanted to write some code that stepped through
    # the servos or motors then this is the Base and size to do that
    SRV_REG_BASE = 0x08
    MOT_REG_BASE = 0x28
    REG_OFFSET = 4

    #to perform a software reset on the PCA chip.
    #Separate from the init function so we can reset at any point if required - useful for development...
    def swReset(self):
        self.i2c.writeto(0,"\x06")

    #setup the PCA chip for 50Hz and zero out registers.
    def initPCA(self):
        self.swReset() #make sure we are in a known position
        #setup the prescale to have 20mS pulse repetition - this is dictated by the servos.
        self.i2c.writeto_mem(108,0xfe,"\x78")
        #block write outputs to off
        self.i2c.writeto_mem(108,0xfa,"\x00")
        self.i2c.writeto_mem(108,0xfb,"\x00")
        self.i2c.writeto_mem(108,0xfc,"\x00")
        self.i2c.writeto_mem(108,0xfd,"\x00")
        #come out of sleep
        self.i2c.writeto_mem(108,0x00,"\x01")

#useful if you need to read the vaules out - but needs ubinascii to make it nice to read.
    #def readMode1Reg():
     #   print(ubinascii.hexlify(i2c.readfrom_mem(108,0,1)))

    #def readPrescaleReg():
     #   print(ubinascii.hexlify(i2c.readfrom_mem(108,0xFE,1)))
        #i2c.readfrom_mem(108,0xFE,1)
    def setPrescaleReg(self):
        i2c.writeto_mem(108,0xfe,"\x78")


    # To get the PWM pulses to the correct size and zero
    # offset these are the default numbers.
    #Servo multiplier is calcualted as follows:
    # 4096 pulses ->20mS 1mS-> count of 204.8
    # 1mS is 90 degrees of travel, so each degree is a count of 204.8/90->2.2755
    # servo pulses always have  aminimum value - so there is guarentees to be a pulse.
    # in the servos Ive examined this is 0.5ms or a count of 102
    #to clauclate the count for the corect pulse is simply:
    # (degrees x count per degree )+ offset 

    def servoWrite(self,servo, degrees):
        #check the degrees is a reasonable number. we expect 0-180, so cap at those values.
        if(degrees>180):
            degrees = 180
        elif (degrees<0):
            degrees = 0
        #check the servo number
        if((servo<1) or (servo>8)):
            raise Exception("INVALID SERVO NUMBER") #harsh, but at least you'll know
        calcServo = self.SRV_REG_BASE + ((servo - 1) * self.REG_OFFSET)
        PWMVal = int((degrees*2.2755)+102) # see comment above for maths
        lowByte = PWMVal & 0xFF
        highByte = (PWMVal>>8)&0x01 #cap high byte at 1 - shoud never be more than 2.5mS.
        self.i2c.writeto_mem(self.CHIP_ADDRESS, calcServo,bytes([lowByte]))
        self.i2c.writeto_mem(self.CHIP_ADDRESS, calcServo+1,bytes([highByte]))


    #Driving the motor is simpler than the servo - just convert 0-100% to 0-4095 and push it to the correct registers.
    #each motor has 4 writes - low and high bytes for a pair of registers. 
    def motorOn(self,motor, direction, speed):
        #cap speed to 0-100%
        if (speed<0):
            speed = 0
        elif (speed>100):
            speed=100
            
        motorReg = self.MOT_REG_BASE + (2 * (motor - 1) * self.REG_OFFSET)
        PWMVal = int(speed * 40.95)
        lowByte = PWMVal & 0xFF
        highByte = (PWMVal>>8) & 0xFF #motors can use all 0-4096
        #print (motor, direction, "LB ",lowByte," HB ",highByte)
        if direction == "f":
            self.i2c.writeto_mem(self.CHIP_ADDRESS, motorReg,bytes([lowByte]))
            self.i2c.writeto_mem(self.CHIP_ADDRESS, motorReg+1,bytes([highByte]))
            self.i2c.writeto_mem(self.CHIP_ADDRESS, motorReg+4,bytes([0]))
            self.i2c.writeto_mem(self.CHIP_ADDRESS, motorReg+5,bytes([0]))
        elif direction == "r":
            self.i2c.writeto_mem(self.CHIP_ADDRESS, motorReg+4,bytes([lowByte]))
            self.i2c.writeto_mem(self.CHIP_ADDRESS, motorReg+5,bytes([highByte]))
            self.i2c.writeto_mem(self.CHIP_ADDRESS, motorReg,bytes([0]))
            self.i2c.writeto_mem(self.CHIP_ADDRESS, motorReg+1,bytes([0]))
        else:
            self.i2c.writeto_mem(self.CHIP_ADDRESS, motorReg+4,bytes([0]))
            self.i2c.writeto_mem(self.CHIP_ADDRESS, motorReg+5,bytes([0]))
            self.i2c.writeto_mem(self.CHIP_ADDRESS, motorReg,bytes([0]))
            self.i2c.writeto_mem(self.CHIP_ADDRESS, motorReg+1,bytes([0]))
            raise Exception("INVALID DIRECTION")
    #To turn off set the speed to 0...
    def motorOff(self,motor):
        self.motorOn(motor,"f",0)
        
    #################
    #Stepper Motors
    #################
    #this is only a basic full stepping.
    #speed sets the length of the pulses (and hence the speed...)
    #so is 'backwards' - the fastest that works reliably with the motors I have to hand is 20mS, but slower than that is good. tested to 2000 (2 seconds per step).
    # motor should be 1 or 2 - 1 is terminals for motor 1 and 2 on PCB, 2 is terminals for motor 3 and 4 on PCB

    def step(self,motor, direction, steps, speed =20, holdPosition=False):

        if(direction =="f"):
            directions = ["f", "r"]
            coils = [((motor*2)-1),(motor*2)]
        elif (direction == "r"):
            directions = ["r", "f"]
            coils = [(motor*2),((motor*2)-1)]
        else:
            raise Exception("INVALID DIRECTION") #harsh, but at least you'll know
        while steps > 0: 
            for direction in directions:
                if(steps == 0):
                    break
                for coil in coils:
                    self.motorOn(coil,direction,100)
                    utime.sleep_ms(speed)
                    steps -=1
                    if(steps == 0):
                        break
    #to save power turn off the coils once we have finished.
    #this means the motor wont hold position.
        if(holdPosition == False):            
            for coil in coils:
                self.motorOff(coil)

    #Step an angle. this is limited by the step resolution - so 200 steps is 1.8 degrees per step for instance.
    # a request for 20 degrees with 200 steps/rev will result in 11 steps - or 19.8 rather than 20.
    def stepAngle(self,motor, direction, angle, speed =20, holdPosition=False, stepsPerRev=200):
        steps = int(angle/(360/stepsPerRev))
        print (steps)
        self.step(motor, direction, steps, speed, holdPosition)
        

    #initialaisation code for using:
        #defaluts to the standard pins and address for the kitronik board, but could be overridden
    def __init__(self, I2CAddress=108,sda=8,scl=9):
        self.CHIP_ADDRESS = 108
        sda=machine.Pin(sda)
        scl=machine.Pin(scl)
        self.i2c=machine.I2C(0,sda=sda, scl=scl, freq=100000)
        self.initPCA()
         
