import Queue
import weigher
import cattEvent
from threading import Thread
import time
import servo

WEIGH_INTERVAL = 1.0
WEIGHT_TRIGGER = 5.0

class cattFeeder(Thread):

	def __init__(self,out = False):
		Thread.__init__(self)
		self.daemon = True
		self.outqueue = out
		self.srv = servo.servo()
		self.inqueue = Queue.Queue()
		self.scales = weigher.weigher()
		self.oldWeight = self.scales.getrealweight()
		self.start()

		
	def run(self):
		while (True):
			try:			
				newCmd = self.inqueue.get(True,WEIGH_INTERVAL)
			except Queue.Empty: #Timeout
				self.checkWeightChange()
			else: #Command received
				self.obeyCommand(newCmd)
				
	def checkWeightChange(self):
		newWeight = self.scales.getrealweight()
		print 'Weight = '+str(newWeight)
		if abs(newWeight-self.oldWeight)>WEIGHT_TRIGGER:
			print "Weight changed by "+str(newWeight-self.oldWeight)
			if self.outqueue:
				self.outqueue.put_nowait(cattEvent.cattEvent("weight_change",newWeight-self.oldWeight))
		self.oldWeight = newWeight

	def obeyCommand(self,cmd):
		if cmd.type == "deliver":
			self.deliverFood(cmd.data)
	
	def deliverFood(self,amount):
		self.srv.home()
		self.srv.oscillate()
		self.srv.home()
		self.srv.idle()
		newWeight = self.scales.getrealweight()
		if self.outqueue:
			self.outqueue.put_nowait(cattEvent.cattEvent("delivered",self.oldWeight-newWeight))
		self.oldWeight = newWeight
