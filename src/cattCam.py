import picamera
import RPIO
import time

IR_EN = True
IR_GPIO = 17
SHUTTER_SPEED = 20000
SENSOR_MODE = 2
RES = (1296,972)
EXP_COMP = -6

class camera:

	def __init__(self,fileroot):
		self.cam = picamera.PiCamera()
		self.cam.led = False
		self.cam.shutter_speed = SHUTTER_SPEED
		self.cam.exposure_compensation = EXP_COMP
		self.cam.resolution = RES
		self.cam.sensor_mode = SENSOR_MODE
		self.fileroot = fileroot
		self.photoIDX = 0
		self.lastphoto = None
		self.lastphototime = None
		if IR_EN:
			RPIO.setup(IR_GPIO,RPIO.OUT)
			RPIO.output(IR_GPIO,False)

	def takephoto(self):
		filename = self.fileroot+str(self.photoIDX)+".jpg"
		self.photoIDX += 1
		if IR_EN:
			RPIO.output(IR_GPIO,True)	
		self.cam.capture(filename)
		self.lastphototime = time.time()
		if IR_EN:
			RPIO.output(IR_GPIO,False)
		self.lastphoto = filename
		return filename

	def getparams(self):
		params = {}
		params['again'] = self.cam.analog_gain+0.0
		params['dgain'] = self.cam.digital_gain+0.0
		params['expsp'] = self.cam.exposure_speed+0.0
		return params

	def __del__(self):
		self.cam.close()
		if IR_EN:
			RPIO.cleanup()
		
	
