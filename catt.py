import PIR
import time
import Queue
import cattWC
import cattTwitter

TWITTER_EN = False
PIR_MSG = "I'm hungry"

eventQueue = Queue.Queue(0)

pir = PIR.PIR()
pir.enableCallback(eventQueue)

WC = cattWC.WC()

if (TWITTER_EN):
	tw = cattTwitter.cattTwitter()

while(True):
	newEvent = eventQueue.get()
	print("New event: "+newEvent.type+" at "+time.strftime("%H:%M:%S",newEvent.time))

	if newEvent.type == "PIR":
		print("PIR triggered")
		imagefile = WC.takephoto()
		if (TWITTER_EN):
			tw.postphoto(PIR_MSG,imagefile)

	if newEvent.type == "weight_change":
		print("Weight changed: "+str(newEvent.data))
		

