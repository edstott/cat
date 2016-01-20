import RPIO
import time
import subprocess

WC_CMD = ["fswebcam","-p","YUYV","-r","352x288","image.jpg"]
GP_CMD = ["gpicview","image.jpg"]
gpicproc = ""

def gpio_callback(gpio_id, val):
	global gpicproc
	print(time.strftime("%H:%M:%S")+": Hello Cat")
	subprocess.call(WC_CMD)
	try:
		gpicproc.kill()
	except AttributeError:
		pass
	gpicproc = subprocess.Popen(GP_CMD)
	
#Copy Xauthority to allow X forwarding
subprocess.call("cp /home/pi/.Xauthority ~/",shell=True)

RPIO.add_interrupt_callback(21,gpio_callback,edge="rising",debounce_timeout_ms=10000)

RPIO.wait_for_interrupts()
