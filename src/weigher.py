import smbus
import time
	
ADC_ADDR = 0x68
CFG_GO = 0x8B
CFG_SLEEP = 0x0B
N_CHANNELS = 4
ADC_SLEEP = 0.1
ADC_CALIBRATION = [-0.056,-0.056,-0.056,-0.056]
ADC_ZERO = 437

class weigher:

	def __init__(self):
		self.i2cbus = smbus.SMBus(1)
		self.i2cbus.write_byte(ADC_ADDR,CFG_SLEEP)
		self.calibrate = ADC_CALIBRATION

	def getrawweight(self):
		rawweight = [0] * N_CHANNELS
		for channel in range(N_CHANNELS):
			adcCfg = CFG_GO | (channel << 5)
			adcword = self.i2cbus.read_word_data(ADC_ADDR,adcCfg)
			time.sleep(ADC_SLEEP)
			adcword = self.i2cbus.read_word_data(ADC_ADDR,CFG_SLEEP)
			#print adcword
			rawweight[channel] = (adcword & 0xff)*0x100+(adcword & 0xff00)/0x100
			if (rawweight[channel]>32767):
				rawweight[channel] -= 65536			

		return(rawweight)

	def getrealweight(self):
		rawweight = self.getrawweight()
		realweight = ADC_ZERO + sum([i*j for (i,j) in zip(rawweight,self.calibrate)])
		return realweight
