import logging
import time,datetime,calendar
import Queue
import PIR
#import cattCam
import cattTwitter
import random
import cattSchedule
import cattFeeder
import cattEvent

TWITTER_EN = True
PIR_MSG = "I'm hungry"
PIR_TWEET_INTERVAL = 900
LOG_FILE = "catt.log"
DEBUG_LEVEL = logging.INFO
IMAGE_ROOT = "img/image_"
SCHED_FILE = "sched.txt"

#Start logging
logging.basicConfig(filename=LOG_FILE,level=DEBUG_LEVEL,format='%(levelname)s %(asctime)s: %(message)s',datefmt='%a, %d %b %Y %H:%M:%S')
consolelog = logging.StreamHandler()
consolelog.setLevel(DEBUG_LEVEL)
consoleformatter = logging.Formatter(fmt='%(levelname)s %(asctime)s: %(message)s',datefmt='%a, %d %b %Y %H:%M:%S')
consolelog.setFormatter(consoleformatter)
logging.getLogger('').addHandler(consolelog)

#Start scheduler
eventQueue = Queue.Queue(0)
CS = cattSchedule.cattSchedule(eventQueue)
CS.addEvent(cattEvent.cattEvent(cattEvent.READ_SCHEDULE,time=time.time()))

#Start feeder
CF = cattFeeder.cattFeeder(eventQueue)

pir = PIR.PIR()
pir.enableCallback(eventQueue)
nextPIRtweettime = 0

#cam = cattCam.camera(IMAGE_ROOT)

if (TWITTER_EN):
	ctw = cattTwitter.cattTwitter()

logging.info('Started catt')

try:
	while(True):
		try:
			newEvent = eventQueue.get(timeout=1000)

		except Queue.Empty:
			pass

		else:
			logging.info("New event: "+newEvent.string()+" at "+time.strftime("%H:%M:%S",time.gmtime(newEvent.time)))

			if newEvent.type == "PIR":
				if (time.time() > nextPIRtweettime):
					nextPIRtweettime = time.time()+PIR_TWEET_INTERVAL
					logging.info("PIR trigger")
					imagefile = cam.takephoto()
					camparams = cam.getparams()
					camparams['again']
					camparams['dgain']
					camparams['expsp']
					logging.info("Took photo %s",imagefile)
					if (TWITTER_EN):
						param_str = ' AG={:0.2f} DG={:0.2f} ES={:0.2f}'.format(camparams['again'],camparams['dgain'],camparams['expsp']/1000)
						ctw.tweetqueue.put(cattTwitter.cattTweet(PIR_MSG,image=imagefile))

			if newEvent.type == "weight_change":
				pass				
				#print("Weight changed: "+str(newEvent.data))

			if newEvent.type == cattEvent.READ_SCHEDULE:
				CS.readSchedule(SCHED_FILE)
				#After reading the file, schedule another read tomorrow
				nextdate = datetime.date.today() + datetime.timedelta(1.0)
				nexttime = calendar.timegm(nextdate.timetuple())
				event = cattEvent.cattEvent(cattEvent.READ_SCHEDULE,time=nexttime)
				CS.addEvent(event)

			if newEvent.type == cattEvent.FEED:
				CF.inqueue.put(newEvent)

except KeyboardInterrupt:
	logging.info('Exit request from console')
	#del cam
	if TWITTER_EN:
		ctw.kill()
	CF.kill()
	CF.join()

except:	#Kill threads on unhandled exceptions
	if TWITTER_EN:
		ctw.kill()
	CF.kill()
	CF.join()
	raise
	
		

