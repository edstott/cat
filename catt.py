import logging
import time
import Queue
import PIR
import cattCam
import cattTwitter

TWITTER_EN = True
PIR_MSG = "I'm hungry"
PIR_TWEET_INTERVAL = 900
LOG_FILE = "catt.log"
DEBUG_LEVEL = logging.INFO
IMAGE_ROOT = "img/image_"

logging.basicConfig(filename=LOG_FILE,level=DEBUG_LEVEL,format='%(levelname)s %(asctime)s: %(message)s',datefmt='%a, %d %b %Y %H:%M:%S')
consolelog = logging.StreamHandler()
consolelog.setLevel(DEBUG_LEVEL)
consoleformatter = logging.Formatter(fmt='%(levelname)s %(asctime)s: %(message)s',datefmt='%a, %d %b %Y %H:%M:%S')
consolelog.setFormatter(consoleformatter)
logging.getLogger('').addHandler(consolelog)

eventQueue = Queue.Queue(0)

pir = PIR.PIR()
pir.enableCallback(eventQueue)
nextPIRtweettime = 0

cam = cattCam.camera(IMAGE_ROOT)

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
			#print("New event: "+newEvent.type+" at "+time.strftime("%H:%M:%S",newEvent.time))

			if newEvent.type == "PIR":
				logging.info("PIR trigger")
				imagefile = cam.takephoto()
				logging.info("Took photo %s",imagefile)
				if (TWITTER_EN and time.time() > nextPIRtweettime):
					ctw.tweetqueue.put(cattTwitter.cattTweet(PIR_MSG,image=imagefile))
					nextPIRtweettime = time.time()+PIR_TWEET_INTERVAL

			if newEvent.type == "weight_change":
				print("Weight changed: "+str(newEvent.data))

except KeyboardInterrupt:
	logging.info('Exit request from console')
	del cam
	if TWITTER_EN:
		ctw.kill()

except:	#Kill threads on unhandled exceptions
	ctw.kill()
	raise
	
		

