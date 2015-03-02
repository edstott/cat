import smbus
	
ADC_ADDR = 0x68
CFG_WORD = 0x1B

class weigher:

	def __init__(self):
		self.i2cbus = smbus.SMBus(0)
		self.i2cbus.write_byte(ADC_ADDR,CFG_WORD)
		self.calibrate = [46,-0.25]

	def getrawweight(self):
		adcword = self.i2cbus.read_word_data(ADC_ADDR,CFG_WORD)
		rawweight = (adcword & 0xff)*0x100+(adcword & 0xff00)/0x100
		if (rawweight>32767):
			rawweight -= 65536
		return(rawweight)

	def getrealweight(self):
		return self.calibrate[0] + self.getrawweight()*self.calibrate[1]
