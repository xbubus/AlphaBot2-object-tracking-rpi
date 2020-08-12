import PCA9685
import time
pca=PCA9685.PCA9685()
pca.setPWMFreq(50)
class Servo():
	def __init__(self,chan=0,centerVal=1457):
		self.pca=pca
		self.pca.setPWMFreq(50)
		self.channel=chan
		self.centerVal=centerVal
		self.currentVal=0
		self.center()
	def center(self):
		self.pca.setServoPulse(self.channel,self.centerVal)
		self.currentVal=self.centerVal
	def checkPosition(self):
		if self.currentVal <=500:
                        self.currentVal=500
                elif self.currentVal >=2500:
                        self.currentVal=2500
	def move(self,val):
		self.currentVal-=val
		self.checkPosition()
		self.pca.setServoPulse(self.channel,self.currentVal)
	def setPosition(self,pos):
		self.currentVal=pos
		self.checkPosition()
		self.pca.setServoPulse(self.channel,self.currentVal)
	def setPositionDegrees(self,deg):
		if deg<(-90):
			deg=-90
		if deg>90:
			deg=90
		if deg>=0:
			self.currentVal=self.centerVal+( deg*(2500-self.centerVal)/90 )
		else:
			self.currentVal=self.centerVal+( deg*(self.centerVal-500)/90)
		self.checkPosition()
		self.pca.setServoPulse(self.channel,self.currentVal)
	def stop(self):
		self.pca.setPWM(self.channel,0,0)
		
if __name__ =='__main__':
	print("main")
	servo=Servo()
	servo.center()
	time.sleep(3)
	servo.setPositionDegrees(-45)
	time.sleep(1)
	servo.setPositionDegrees(45)
	time.sleep(1)
	servo.setPositionDegrees(90)
	time.sleep(1)
	servo.setPositionDegrees(-90)
	time.sleep(1)
	servo.stop()
	time.sleep(1) 
	servo2=Servo(chan=1,centerVal=1800)
	servo2.center()
	time.sleep(1)
	servo2.stop()
   
       
