import smbus

class weigher:
	
	ADC_ADDR = 0x68
	CFG_WORD = 0x1B

	def __init__(self):
		self.i2cbus = smbus.SMBus(0)
		self.i2cbus.write_byte(ADC_ADDR,CFG_WORD)

	def getweight(self):
		adcword = self.i2cbus.read_word_data(ADC_ADDR,CFG_WORD)
		rawweight = (adcword & 0xff)*0x100+(adcword & 0xff00)/0x100
		if (rawweight>32767):
			rawweight -= 65536
		return(rawweight)
