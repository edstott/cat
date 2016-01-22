import logging
import time,datetime,calendar
import Queue
import random

import PIR
import cattCam
import cattTwitter
import cattSchedule
import cattFeeder
import cattEvent
import cattWeb

LOG_FILE = "catt.log"
DEBUG_LEVEL = logging.DEBUG

class catt:

	TWITTER_EN = False
	CAM_EN = True
	WEB_EN = True
	PIR_MSG = "I'm hungry"
	FED_MSG = "I've been given {:f}g of food"

	PIR_TWEET_INTERVAL = 900
	IMAGE_ROOT = "../img/image_"
	SCHED_FILE = "sched.txt"

	WEB_INTERVAL = datetime.timedelta(minutes = 10)
	
	STATS_DICT = {'fed':0.0, 'pir_trig':0, 'date':None, 'tweets':0, 'start_weight':0.0, 'end_weight':0.0}
	
	def __init__(self):
		logging.info('Started catt')
		self.eventQueue = Queue.Queue(0)
		
		#Start twitter
		if (catt.TWITTER_EN):
			self.ctw = cattTwitter.cattTwitter(self.eventQueue)
						
		#Start scheduler
		self.CS = cattSchedule.cattSchedule(self.eventQueue)
		self.CS.addEvent(cattEvent.cattEvent(cattEvent.READ_SCHEDULE,time=time.time()))			
		#Schedule a stats update at midnight
		nextdate = datetime.date.today() + datetime.timedelta(1.0)
		nexttime = calendar.timegm(nextdate.timetuple())
		event = cattEvent.cattEvent(cattEvent.UPDATE_STAT,time=nexttime)
		self.CS.addEvent(event)
		#Schedule web page update
		if catt.WEB_EN:
			self.CS.addEvent(cattEvent.cattEvent(cattEvent.UPDATE_WEB,time=time.time()))	
				
		#Start feeder
		self.CF = cattFeeder.cattFeeder(self.eventQueue)
		
		#Start PIR
		self.pir = PIR.PIR()
		self.pir.enableCallback(self.eventQueue)
		self.nextPIRtweettime = 0

		#Setup Web
		if catt.WEB_EN:
			self.CW = cattWeb.cattWeb()
		
		if catt.CAM_EN:
			self.cam = cattCam.camera(catt.IMAGE_ROOT)
		
		self.todaystat = catt.STATS_DICT
		self.todaystat['date'] = datetime.date.today()
		self.oldstat = []
			
	def eventLoop(self):

		while(True):
			try:	#Need to use a timeout so that KeyboardInterrupt exception gets through
				newEvent = self.eventQueue.get(timeout=1000)
			except Queue.Empty:
				pass
			else:
				self.processEvent(newEvent)
			
	def processEvent(self,newEvent):
		logging.info("New event: "+newEvent.string()+" at "+time.strftime("%H:%M:%S",time.gmtime(newEvent.time)))

		if newEvent.type == "PIR":
			if (time.time() > self.nextPIRtweettime):
				self.nextPIRtweettime = time.time()+catt.PIR_TWEET_INTERVAL
				logging.info("PIR trigger")
				self.todaystat['pir_trig'] += 1
				if catt.CAM_EN:
					imagefile = self.cam.takephoto()
					#camparams = self.cam.getparams()
					#camparams['again']
					#camparams['dgain']
					#camparams['expsp']
					logging.info("Took photo %s",imagefile)
				if (catt.TWITTER_EN):
					if catt.CAM_EN:
						#param_str = ' AG={:0.2f} DG={:0.2f} ES={:0.2f}'.format(camparams['again'],camparams['dgain'],camparams['expsp']/1000)
						self.ctw.tweetqueue.put(cattTwitter.cattTweet(catt.PIR_MSG,image=imagefile))
					else:
						self.ctw.tweetqueue.put(cattTwitter.cattTweet(catt.PIR_MSG))

		if newEvent.type == cattEvent.WEIGHT_CHANGE:
			self.todaystat['end_weight'] += newEvent.data

		if newEvent.type == cattEvent.READ_SCHEDULE:
			self.CS.readSchedule(catt.SCHED_FILE)
			#After reading the file, schedule another read tomorrow
			nextdate = datetime.date.today() + datetime.timedelta(1.0)
			nexttime = calendar.timegm(nextdate.timetuple())
			event = cattEvent.cattEvent(cattEvent.READ_SCHEDULE,time=nexttime)
			self.CS.addEvent(event)

		if newEvent.type == cattEvent.FEED:
			self.CF.inqueue.put(newEvent)
			
		if newEvent.type == cattEvent.DELIVERED:
			self.todaystat['fed'] += newEvent.data
			self.todaystat['end_weight'] += newEvent.data
			if catt.TWITTER_EN:
				self.ctw.tweetqueue.put(cattTwitter.cattTweet(catt.FED_MSG.format(newEvent.data)))
				
		if newEvent.type == cattEvent.UPDATE_WEB:
			if catt.WEB_EN:
				self.CW.update(self)
				#Schedule next web update
				nexttime = calendar.timegm((datetime.datetime.utcnow()+catt.WEB_INTERVAL).timetuple())
				event = cattEvent.cattEvent(cattEvent.UPDATE_WEB,time=nexttime)
				self.CS.addEvent(event)
				
		if newEvent.type == cattEvent.UPDATE_STAT:
			current_weight = self.todaystat['end_weight']
			self.oldstat += self.todaystat
			self.todaystat = catt.STATS_DICT
			self.todaystat['date'] = datetime.date.today()
			self.todaystat['start_weight'] = current_weight
			self.todaystat['end_weight'] = current_weight
			#Schedule another update tomorrow
			nextdate = datetime.date.today() + datetime.timedelta(1.0)
			nexttime = calendar.timegm(nextdate.timetuple())
			event = cattEvent.cattEvent(cattEvent.UPDATE_STAT,time=nexttime)
			self.CS.addEvent(event)
			
		if newEvent.type == cattEvent.SENT_TWEET:
			self.todaystat['tweets'] += 1
			

	def kill(self):
		if catt.TWITTER_EN:
			self.ctw.kill()
		self.CF.kill()
		self.CF.join()

if __name__ == '__main__':
	#Start logging
	logging.basicConfig(filename=LOG_FILE,level=DEBUG_LEVEL,format='%(levelname)s %(asctime)s: %(message)s',datefmt='%a, %d %b %Y %H:%M:%S')
	consolelog = logging.StreamHandler()
	consolelog.setLevel(DEBUG_LEVEL)
	consoleformatter = logging.Formatter(fmt='%(levelname)s %(asctime)s: %(message)s',datefmt='%a, %d %b %Y %H:%M:%S')
	consolelog.setFormatter(consoleformatter)
	logging.getLogger('').addHandler(consolelog)
	
	#Create catt class
	
	try:
		C = catt()
		C.eventLoop()
		
	except KeyboardInterrupt:
		logging.info('Exit request from console')
		C.kill()
		#del cam

	except:	#Kill threads on unhandled exceptions
		logging.exception('Error')
		C.kill()
		raise
	
		

