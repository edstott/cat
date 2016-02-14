
from RPi import GPIO
import time

DEF_PRD = 0.020
DEF_PIN = 18
MIN_PULSE = 0.0007
MAX_PULSE = 0.0024
DEF_HOME = 0.5

class servo(GPIO.PWM):
	def __init__(self, period=DEF_PRD, pin=DEF_PIN, home=DEF_HOME):
		self.period = period
		self.pin = pin
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.pin,GPIO.OUT)
		GPIO.PWM.__init__(self,self.pin,1/self.period)
		self.min = MIN_PULSE
		self.max = MAX_PULSE
		self.homeAng = home
		self.isRunning = False

	def setAngle(self,angle):
		if self.isRunning:
			self.ChangeDutyCycle(self.convertAngletoDC(angle))
		else:
			self.start(self.convertAngletoDC(angle))
			self.isRunning = True

	def home(self):
		self.setAngle(self.homeAng)

	def convertAngletoDC(self, angle):
		DC = (self.min+(self.max-self.min)*angle)/self.period*100
		return DC

	def idle(self):
		self.isRunning = False
		self.stop()

	def oscillate(self, amplitude=0.1, cycles=1, period=2.0):
		self.setAngle(self.homeAng+amplitude)
		for i in xrange(cycles):
			self.setAngle(self.homeAng+amplitude)
			time.sleep(period/2.0)
			self.setAngle(self.homeAng)
			time.sleep(period/2.0)

	def kill(self):
		self.isRunning = False
		self.stop()
		GPIO.setup(self.pin,GPIO.IN)
		
		
		
			
		
