




from robot import Robot
import time
class Logic():
	def __init__(self):
		self.robot=Robot()
		self.wasPreviousOffsetPositive=True
		self.defaultPWM=30
		self.debugVal=850  # for calibraiting gain
                self.k=self.defaultPWM/(320.0+self.debugVal)
		print("k",self.k)
		self.ki=0 #self.k*0.5
		self.kd=self.k*0.4
		self.prev_error=0
		self.error_sum=0
		self.center=320
                self.centerR=320+55
                self.centerL=320-55
		self.error=0
		self.errorI=0
		self.errorD=0
		self.pwm=0
		self.prev_off=0
		self.pTerm=0
		self.dTerm=0
		self.was_forward=True
	def rotationOnlyHandler(self):
		pass
	def handleXoffset(self,offset):
		if offset>0:
#			robot.servoLR.move(10)
			if offset>35:
				self.wasPreviousOffsetPositive=True
				self.robot.stepRight()
		if offset<0:
#			robot.servoLR.move(-10)
			if offset<-35:
				self.wasPreviusOffsetPositive=False
				self.robot.stepLeft()
	def handleRadius(self,radius,offset):
		if offset <= 30 and offset >= -30:
			if radius <150 and radius >30:
				self.robot.stepForward()
			elif radius >250:
				self.robot.stepBackward()
		if radius==0:
			if self.wasPreviousOffsetPositive:
				self.robot.stepLeft()	
			else:
				self.robot.stepRight()

	def handleYoffset(self,offset):
		if offset>30:
			self.robot.servoUD.move(-10) 
		elif offset<-30:
			self.robot.servoUD.move(10)
		else:
			self.robot.servoUD.stop()
	def handleV2(self,xoff,yoff,radius):
		self.handleYoffset(yoff)
		if radius==0 or radius>200:
			self.robot.stop()
			return
		if xoff>self.centerR-self.center or xoff<self.centerL-self.center:
			
			self.error=xoff
			self.error_sum+=self.error
			self.errorD=self.error-self.prev_error
			self.prev_error=self.error
			self.pTerm=abs(int(self.error*self.k))
			self.dTerm=abs(int(self.errorD*self.kd))
			if self.prev_error==0:
				self.dTerm=0
			self.pwm=self.defaultPWM+self.pTerm+self.dTerm
			self.prev_off=xoff
			self.was_forward=False
			if xoff<0: #left
				print ("ball is on left",self.pwm)
				if radius>100 and xoff<-100:
					self.robot.updatePWM(self.defaultPWM,25)
				else:
					self.robot.updatePWM(self.pwm,self.defaultPWM)
			elif xoff>0: #right
				print("ball is on right",self.pwm)
				if radius >100 and xoff>100:
					self.robot.updatePWM(25,self.defaultPWM)
				else:
					self.robot.updatePWM(self.defaultPWM,self.pwm)
		elif radius>0:
			self.error_sum=0
			if radius<180:
				self.was_forward=True
				print("going forward")
				self.robot.updatePWM(self.defaultPWM,self.defaultPWM)
			else:	
				print("stoping")
				self.robot.stop()

			
