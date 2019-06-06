import pyb
class TrackingFSM:
	"""对象追踪状态机。

	该类负责实现通过综合一个时间窗口内的数据来断言目标是否被锁定。

	"""
	IDLE = 0 #: 空闲状态

	LOCKING = 1	#: 锁定状态
	
	RELAX_IN = 2#: 确认锁定状态
	
	RELAX_OUT = 3#: 确认失锁状态
	def __init__(self,relaxInDelay = 500,relaxOutDelay =500):
		"""对象追踪状态机的构造函数
		
		:param relaxInDelay: 进入延迟时间, defaults to 500
		:type relaxInDelay: int, optional
		:param relaxOutDelay: 失锁延迟时间, defaults to 500
		:type relaxOutDelay: int, optional
		"""
		self.__InnerFSM=self.IDLE
		self.__relaxInTimPin  = 0
		self.__relaxOutTimPin  = 0
		self.__relaxOutDelay = relaxOutDelay
		self.__relaxInDelay=relaxInDelay
	def feed(self,objectInfo):
		"""流数据输入接口。负责内部状态机的状态转移

		.. graphviz:: 

			digraph G {
				IDLE [label = "空闲"]
				LOCKING[label = "锁定"]
				RIN [label = "确认锁定"]
				ROUT [label = "确认失锁"]

				IDLE ->RIN [label = "Captured"]
				RIN->LOCKING [label = "Timeout"]
				RIN->RIN[label = "Tick"]
				RIN->IDLE[label = "Lost"]

				LOCKING->ROUT[label = "Lost"]
				ROUT->LOCKING[label = "Caotured"]
				ROUT->IDLE[label = "Timeout"]
				ROUT->ROUT[label = "Tick"]

			}
		

		该函数应该被连续调用，以传入实时图像数据
		
		:param objectInfo: 对象追踪信息
		:type objectInfo: False|Tuple
		"""
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
		"""获得当前状态机的状态信息
		
		:return: 当前状态代号
		:rtype: int
		"""
		return self.__InnerFSM
	def getStateStr(self):
		"""获取当前状态机的状态信息的自然语言描述
		
		:return: 当前状态描述
		:rtype: str
		"""
		if self.__InnerFSM == self.IDLE:
			return "IDLE"
		elif self.__InnerFSM == self.LOCKING:
			return "LOCKING"
		elif self.__InnerFSM == self.RELAX_IN:
			return "RIN"
		elif self.__InnerFSM == self.RELAX_OUT:
			return "ROUT"
		return "None"
