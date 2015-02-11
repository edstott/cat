import os
import twitter
import RPIO
import time
import subprocess

TWITTER_CREDS = os.path.expanduser('~/.catt_credentials')
CONSUMER_KEY = "eRENCvbmZ1mfSSyis9uVMstGb"
CONSUMER_SECRET = "meWNE4ndZ33LNCarMUnwhI1OKZU06c1HdsfxGKzihaAoffWga1"

IMAGE_FILE = "image.jpg"
WC_CMD = ["fswebcam","-p","YUYV","-r","352x288",IMAGE_FILE]
GP_CMD = ["gpicview",IMAGE_FILE]
gpicproc = ""

def gpio_callback(gpio_id, val):
	global gpicproc,twitter
	print(time.strftime("%H:%M:%S")+": Hello Cat")
	subprocess.call(WC_CMD)
	try:
		gpicproc.kill()
	except AttributeError:
		pass
	gpicproc = subprocess.Popen(GP_CMD)
	with open(IMAGE_FILE,"rb") as imagefile:
		tparams = {"media[]":imagefile.read(),"status":"I'm hungry"}
	twitter.statuses.update_with_media(**tparams)


#Initialise Twitter
if not os.path.exists(TWITTER_CREDS):
	twitter.oauth_dance("My App Name", CONSUMER_KEY,CONSUMER_SECRET,TWITTER_CREDS)

oauth_token, oauth_secret = twitter.read_token_file(TWITTER_CREDS)

twitter = twitter.Twitter(auth=twitter.OAuth(oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))

#Copy Xauthority to allow X forwarding
subprocess.call("cp /home/pi/.Xauthority ~/",shell=True)

#Setup PIR interrupt
RPIO.add_interrupt_callback(21,gpio_callback,edge="rising",debounce_timeout_ms=10000)

try:
	RPIO.wait_for_interrupts()
except KeyboardInterrupt:
	pass

print("Exiting")
quit()




