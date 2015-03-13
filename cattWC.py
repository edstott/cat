import subprocess
import os

FILE_PREFIX = "image_"
WC_CMD = ["fswebcam","-p","YUYV","-r","352x288"]

class WC:

	def __init__(self):
		self.photoIDX = 0

	def takephoto(self):
		filename = FILE_PREFIX+str(self.photoIDX)+".jpg"
		self.photoIDX += 1
		subprocess.call(WC_CMD+[filename],stderr=open(os.devnull, 'wb'))
		return filename
	
