import pyb
class TrackingFSM:
	IDLE = 0
	LOCKING = 1
	RELAX_IN = 2
	RELAX_OUT = 3
	def __init__(self,relaxInDelay = 500,relaxOutDelay =500):
		self.__InnerFSM=self.IDLE
		self.__relaxInTimPin  = 0
		self.__relaxOutTimPin  = 0
		self.__relaxOutDelay = relaxOutDelay
		self.__relaxInDelay=relaxInDelay
	def feed(self,objectInfo):
		if self.__InnerFSM == self.IDLE:
			if objectInfo != False:
				self.__InnerFSM = self.RELAX_IN
				self.__relaxInTimPin = pyb.millis()
		elif self.__InnerFSM == self.LOCKING:
			if  objectInfo == False:
				self.__InnerFSM = self.RELAX_OUT
				self.__relaxOutTimPin = pyb.millis()
		elif self.__InnerFSM == self.RELAX_IN:
			if  objectInfo == False:
				self.__InnerFSM = self.IDLE
			else:
				if pyb.millis()-self.__relaxInTimPin>self.__relaxInDelay:
					self.__InnerFSM = self.LOCKING
		elif self.__InnerFSM == self.RELAX_OUT:
			if  objectInfo != False:
				self.__InnerFSM = self.LOCKING
			else:
				if pyb.millis()-self.__relaxOutTimPin>self.__relaxOutDelay:
					self.__InnerFSM = self.IDLE
	def getState(self):
		return self.__InnerFSM
	def getStateStr(self):
		if self.__InnerFSM == self.IDLE:
			return "IDLE"
		elif self.__InnerFSM == self.LOCKING:
			return "LOCKING"
		elif self.__InnerFSM == self.RELAX_IN:
			return "RIN"
		elif self.__InnerFSM == self.RELAX_OUT:
			return "ROUT"
		return "None"
