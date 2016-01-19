import Queue
import weigher
import cattEvent
from threading import Thread
import time
import servo

WEIGH_INTERVAL = 1.0
WEIGHT_TRIGGER = 5.0

MAX_FEED_TRIES = 20
FEED_AMP = 0.10
STABLE_DELAY = 1.0

enableFeed = True

class cattFeeder(Thread):

	def __init__(self,out = False):
		Thread.__init__(self)
		self.outqueue = out
		self.srv = servo.servo()
		self.inqueue = Queue.Queue()
		self.scales = weigher.weigher()
		self.oldWeight = self.scales.getrealweight()
		self.start()

	#Thread loop - wait for command in the queue, weigh the silo	
	def run(self):
		self.stop = False
		while not self.stop:
			try:			
				newCmd = self.inqueue.get(True,WEIGH_INTERVAL)
			except Queue.Empty: #Timeout
				self.checkWeightChange()
			else: #Command received
				self.obeyCommand(newCmd)
	
	#Correct for weight drift on every timed measurement. Flag abrupt changes			
	def checkWeightChange(self):
		newWeight = self.scales.getrealweight()
		#print 'Weight = '+str(newWeight)
		if abs(newWeight-self.oldWeight)>WEIGHT_TRIGGER:
			#print "Weight changed by "+str(newWeight-self.oldWeight)
			if self.outqueue:
				self.outqueue.put_nowait(cattEvent.cattEvent(cattEvent.WEIGHT_CHANGE,newWeight-self.oldWeight))
		self.oldWeight = newWeight

	#Command handler
	def obeyCommand(self,cmd):
		if cmd.type == cattEvent.FEED:
			#print "Feeding " + str(cmd.data)
			if enableFeed:
				self.deliverFood(cmd.data)
		if cmd.type == "kill":
			self.srv.kill()
			self.stop = True
			
	#Deliver requested amount of food by operating servo and weighing silo
	def deliverFood(self,amount):
		initialweight = self.scales.getrealweight()
		targetweight = initialweight - amount
		feedloop = True
		self.srv.home()
		tries = 0
	
		while feedloop:					
			self.srv.oscillate(cycles=1, amplitude=FEED_AMP)
			tries += 1
			time.sleep(STABLE_DELAY)
			intWeight = self.scales.getrealweight()
			#print str(intWeight)
			if intWeight <= targetweight:
				feedloop = False
			if tries > MAX_FEED_TRIES:
				feedloop = False

		self.srv.home()
		self.srv.idle()
		newWeight = self.scales.getrealweight()
		diffWeight = initialweight - newWeight
		print "Delivered " + str(diffWeight)
		if self.outqueue:
			self.outqueue.put_nowait(cattEvent.cattEvent(cattEvent.DELIVERED,diffWeight))
		self.oldWeight = newWeight

	#Put a thread kill command on the queue, wait for thread to end
	def kill(self):
		self.inqueue.put_nowait(cattEvent.cattEvent("kill"))
		#self.join()

	#Put a deliver command on the queue
	def feed(self,amount):
		self.inqueue.put_nowait(cattEvent.cattEvent("deliver",amount))

