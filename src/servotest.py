import RPi.GPIO as GPIO
import time

PERIOD = 0.02
SLEEP = 0.1
MIN_PRD = 0.0007
MAX_PRD = 0.0024


try:
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(18,GPIO.OUT)
	pwm = GPIO.PWM(18,1/PERIOD)
	Dir = 1
	Angle = 0
	DC = (MIN_PRD+(MAX_PRD-MIN_PRD)*Angle)/PERIOD
	pwm.start(DC)

	while True:
		if Dir:
			Angle += 0.01
			if Angle >= 1:
				Dir = 0
		else:
			Angle -= 0.01
			if Angle <= 0:
				Dir = 1
		
		DC = (MIN_PRD+(MAX_PRD-MIN_PRD)*Angle)/PERIOD*100
		pwm.ChangeDutyCycle(DC)
		time.sleep(SLEEP)
	
except:
	GPIO.cleanup()
	raise
