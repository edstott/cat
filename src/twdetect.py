import os
import twitter
import RPIO
import time
import subprocess

#GPIO
PID_GPIO = 21
PID_REARM = 10000

#Twitter
TWITTER_CREDS = os.path.expanduser('~/.catt_credentials')
CONSUMER_KEY = "eRENCvbmZ1mfSSyis9uVMstGb"
CONSUMER_SECRET = "meWNE4ndZ33LNCarMUnwhI1OKZU06c1HdsfxGKzihaAoffWga1"
PID_STATUS = "I'm hungry"

#Image Capture
IMAGE_FILE = "image.jpg"
WC_CMD = ["fswebcam","-p","YUYV","-r","352x288",IMAGE_FILE]
GP_CMD = ["gpicview",IMAGE_FILE]
gpicproc = ""

def gpio_callback(gpio_id, val):
	global gpicproc,twitter
	print(time.strftime("%H:%M:%S")+": "+PID_STATUS)
	subprocess.call(WC_CMD)
	try:
		gpicproc.kill()
	except AttributeError:
		pass
	gpicproc = subprocess.Popen(GP_CMD)
	with open(IMAGE_FILE,"rb") as imagefile:
		tparams = {"media[]":imagefile.read(),"status":PID_STATUS}
	twitter.statuses.update_with_media(**tparams)


#Initialise Twitter
if not os.path.exists(TWITTER_CREDS):
	twitter.oauth_dance("Catt", CONSUMER_KEY,CONSUMER_SECRET,TWITTER_CREDS)

oauth_token, oauth_secret = twitter.read_token_file(TWITTER_CREDS)

twitter = twitter.Twitter(auth=twitter.OAuth(oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))

#Copy Xauthority to allow X forwarding
subprocess.call("cp /home/pi/.Xauthority ~/",shell=True)

#Setup PIR interrupt
RPIO.add_interrupt_callback(PID_GPIO,gpio_callback,edge="rising",debounce_timeout_ms=PID_REARM)

try:
	RPIO.wait_for_interrupts()
except KeyboardInterrupt:
	pass

print("Exiting")
try:
	gpicproc.kill()
except AttributeError:
	pass
quit()




