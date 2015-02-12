import RPIO
import Queue
import weigher
import cattEvent

WEIGH_INTERVAL = 10.0

class cattFeeder:

	def __init__(self,outqueue):
		self.servo = RPIO.PWM.Servo()
		self.outqueue = outqueue
		self.inqueue = Queue.Queue
		self.scales = weigher.weigher
		self.oldWeight = self.weigher.getweight()
		thre
		
	def feederService(self):
		while (True):
			try:			
				newCmd = self.inqueue.get(True,WEIGH_INTERVAL)
			except Queue.Empty: #Timeout
				self.checkWeightChange()
			else: #Command received
				self.obeyCommand(newCmd)
				
	def checkWeightChange(self):
		newWeight = self.weigher.getweight()
		if abs(newWeight-self.oldWeight)>WEIGHT_TRIGGER:
			self.outqueue.put_nowait(cattEvent.cattEvent("weight_change",newWeight-self.oldWeight))
		self.oldWeight = newWeight

	def obeyCommand(self,cmd):
		if cmd.type == "deliver":
			self.deliverFood(cmd.data)
	
	def deliverFood(self,amount):
		self.outqueue.put_nowait(cattEvent.cattEvent("delivered",newWeight-self.amount))
