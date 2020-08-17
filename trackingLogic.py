from robot import Robot
import time

class Logic():
	def __init__(self):
		self.robot=Robot()
		self.defaultPWM=30
		self.debugVal=950  # for calibraiting gain
		self.kp=self.defaultPWM/(320.0+self.debugVal)
		print("k",self.kp) 
		self.kd=self.kp*0.6
		self.prev_error=0
		self.max_offset=55
		self.error=0
		self.errorD=0
		self.pwm=0
		self.pTerm=0
		self.dTerm=0
	def rotationOnlyHandler(self):
		pass
	def handleXoffset(self,offset): #ball on the right -> do step right... not used in handleV2
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
	def handleRadius(self,radius,offset): #move forward or backward to increase/decrease ball radius
	#not used in handleV2
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

	def handleYoffset(self,offset): #move servo up-down depending of position of the center of ball
		if offset>30:
			self.robot.servoUD.move(-10) 
		elif offset<-30:
			self.robot.servoUD.move(10)
		else:
			self.robot.servoUD.stop()
			
	def handleV2(self,xoff,yoff,radius):
		self.handleYoffset(yoff)
		if radius==0 or radius>180:
			self.robot.stop()
			return
		if abs(xoff)>self.max_offset: # ball is not in the center
			self.error=xoff
			self.errorD=self.error-self.prev_error
			self.prev_error=self.error
			self.pTerm=abs(int(self.error*self.kp))
			self.dTerm=abs(int(self.errorD*self.kd))
			self.pwm=self.defaultPWM+self.pTerm+self.dTerm
			if xoff<0: #ball is on left
				print ("ball is on left",self.pwm)
				self.robot.updatePWM(self.pwm,self.defaultPWM)
			elif xoff>0: #ball is on right
				print("ball is on right",self.pwm)
				self.robot.updatePWM(self.defaultPWM,self.pwm)
		elif radius<180:
			self.was_forward=True
			print("going forward")
			self.robot.updatePWM(self.defaultPWM,self.defaultPWM)
		else:	
			print("stoping")
			self.robot.stop()

			
