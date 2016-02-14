import Queue
import weigher
import cattEvent
from threading import Thread
import time
import logging
import servo

WEIGH_INTERVAL = 10.0
WEIGHT_TRIGGER = 5.0
WEIGHT_TOLERANCE = 3.0
MAX_FEED_TRIES = 20
FEED_AMP_INIT = 0.02	#Initial feeder amplitude
FEED_AMP_INC = 0.01	#Feeder amplitude increment if no weight change
FEED_AMP_MAX = 0.20	#Maximum feeder amplitude
FEED_CENTRE = 0.40	#Feeder home position
STABLE_DELAY = 4.0	#Delay after each feed attempt before weighing
AMP_BOOST_WT = 1.0	#Minimum delivery weight to persist at current amplitude

enableFeed = True

class cattFeeder(Thread):

	def __init__(self,out = False):
		Thread.__init__(self)
		self.outqueue = out
		self.srv = servo.servo(home=FEED_CENTRE)
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
		if cmd.type == cattEvent.KILL:
			self.srv.kill()
			self.stop = True
			
	#Deliver requested amount of food by operating servo and weighing silo
	def deliverFood(self,amount):
		initialweight = self.scales.getrealweight()
		targetweight = initialweight - amount
		logging.info("%fg of food has been requested",amount)
		feedloop = True
		self.srv.home()
		tries = 0
		amp = FEED_AMP_INIT
		lastWeight = initialweight
	
		while feedloop:
			self.srv.oscillate(cycles=1, amplitude=amp)
			tries += 1
			time.sleep(STABLE_DELAY)
			intWeight = self.scales.getrealweight()
			logging.debug("Feed attempt %d at ampl. %f. %f delivered",tries,amp,lastWeight-intWeight)				

			#Was any food delivered at all? Increase amplitude if not
			if lastWeight-intWeight < AMP_BOOST_WT:
				amp = min(amp + FEED_AMP_INC,FEED_AMP_MAX)

			#Has the target amount been delivered? Finish if so
			if intWeight <= targetweight:
				feedloop = False

			#Has the maximum iteration count been reached? Finish if so
			if tries > MAX_FEED_TRIES:
				feedloop = False

			lastWeight = intWeight

		self.srv.home()
		self.srv.idle()
		newWeight = self.scales.getrealweight()
		diffWeight = initialweight - newWeight
		logging.info("Delivered %fg after %d pulses",diffWeight,tries)
		if self.outqueue:
			self.outqueue.put_nowait(cattEvent.cattEvent(cattEvent.DELIVERED,diffWeight))
			if abs(diffWeight - amount) > WEIGHT_TOLERANCE:
				self.outqueue.put_nowait(cattEvent.cattEvent(cattEvent.FEED_ERROR,(targetweight-diffWeight)))
		self.oldWeight = newWeight

	#Put a thread kill command on the queue, wait for thread to end
	def kill(self):
		self.inqueue.put_nowait(cattEvent.cattEvent(cattEvent.KILL))
		#self.join()

	#Put a deliver command on the queue
	def feed(self,amount):
		self.inqueue.put_nowait(cattEvent.cattEvent(cattEvent.FEED,amount))

