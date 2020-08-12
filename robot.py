

import RPi.GPIO as GPIO
import motor
import time
import servos
import time

SPEED_VAR_LR=0.002
SPEED_VAR_FB=0.01 # zrobic cos z tym

def getch():
    import termios
    import sys, tty
    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    return _getch()

class Robot(object):
    
    def __init__(self,in1=13,in2=12,ena=6,in3=21,in4=20,enb=26):
       self.motorL=motor.Motor(in1,in2,ena) #motor LEFT
       self.motorR=motor.Motor(in3,in4,enb) #motor RIGHT
       self.servoLR=servos.Servo() #servo LEFT RIGHT
       self.servoUD=servos.Servo(chan=1,centerVal=1800)
       self.servoUD.stop()
       self.stop() #servo UP DOWN
    def stepRight(self):
       self.motorL.forward()
       self.motorR.backward()
       time.sleep(SPEED_VAR_LR)  
       self.motorL.stop()
       self.motorR.stop()
    def stepLeft(self):
       self.motorR.forward()
       self.motorL.backward()
       time.sleep(SPEED_VAR_LR)
       self.motorR.stop()
       self.motorL.stop()
    def stepForward(self):
       self.motorL.forward()
       self.motorR.forward()
       time.sleep(SPEED_VAR_FB)
       self.motorL.stop()
       self.motorR.stop()
    def stepBackward(self):
       self.motorL.backward()
       self.motorR.backward()
       time.sleep(SPEED_VAR_FB)
       self.motorL.stop()
       self.motorR.stop()
    def stop(self):
       self.motorL.stop()
       self.motorR.stop()
    def updatePWM(self,r_pwm,l_pwm):
       self.motorL.setPWM(l_pwm)
       self.motorR.setPWM(r_pwm)
    def goForward(self):
       self.motorL.forward()
       self.motorR.forward()
    def goBackward(self):
       self.motorL.backward()
       self.motorR.backward()
    def goLeft(self):
       self.motorL.backward()
       self.motorR.forward()
    def goRight(self):
       self.motorL.forward()
       self.motorR.backward()   				      
	       
if __name__=='__main__':
	robot=Robot()
	robot.motorL.setPWM(50)
    	robot.motorR.setPWM(50)
	robot.stop()
    	robot.servoLR.center()
    	robot.servoUD.center()
    	time.sleep(0.5)
    	robot.servoUD.stop()
    	robot.servoLR.stop()
    	try:
		while True:
			print("Enter command:\n")
			value=getch()
			print(value)
			if value=="q":
				robot.motorL.stop()
        	        	robot.motorR.stop()
        	    	elif value=="w":
	                	robot.motorL.forward()
        	        	robot.motorR.forward()
            		elif value=="d":
				robot.motorL.forward()
				robot.motorR.stop()
		    	elif value=="a":
				robot.motorR.forward()
				robot.motorL.stop()
		    	elif value=="s":
				robot.motorR.backward()
				robot.motorL.backward()
	            	elif value=="t":
        	        	robot.stepForward()
            		elif value=="f":
                		robot.stepLeft()
         	   	elif value=="h":
                		robot.stepRight()
	    		elif value=="i":
				robot.servoUD.move(20)
	    		elif value=="k":
	        		robot.servoUD.move(-20)
	    		elif value=="l":
				robot.servoLR.move(20)
	    		elif value=="j":
				robot.servoLR.move(-20)
	    		elif value=="x":
				robot.servoUD.stop()
				robot.servoLR.stop()
	                	robot.motorR.stop()
        	        	robot.motorL.stop()
                		GPIO.cleanup()
				break	    
     #  	     		time.sleep(0.2)
	except KeyboardInterrupt:
		robot.servoUD.stop()
            	robot.servoLR.stop()
	    	robot.motorR.stop()
	    	robot.motorL.stop()
            	GPIO.cleanup()
