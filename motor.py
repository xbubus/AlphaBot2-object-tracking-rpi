import RPi.GPIO as GPIO


class Motor(object):
    def __init__(self,in1,in2,en):
        self.IN1=in1
        self.IN2=in2
        self.EN=en
        self.P=30
        GPIO.setmode(GPIO.BCM)
    	GPIO.setwarnings(False)
        GPIO.setup(self.IN1,GPIO.OUT)
    	GPIO.setup(self.IN2,GPIO.OUT)
    	GPIO.setup(self.EN,GPIO.OUT)
        self.PWM=GPIO.PWM(self.EN,500)
        self.PWM.start(self.P)
    	GPIO.output(self.IN1,GPIO.HIGH)
        GPIO.output(self.IN2,GPIO.LOW)
    	self.stop()

    def stop(self):
	    self.PWM.ChangeDutyCycle(0)
    def forward(self): 
	    GPIO.output(self.IN1,GPIO.HIGH)
	    GPIO.output(self.IN2,GPIO.LOW)
    def backward(self):
	    GPIO.output(self.IN1,GPIO.LOW)
	    GPIO.output(self.IN2,GPIO.HIGH)
    def setPWM(self,value):
	    self.P = value
	    self.PWM.ChangeDutyCycle(self.P)
    
    
