import smbus
import time

ADC_ADDR = 0x68
CFG_WORD = 0x1B

i2cbus = smbus.SMBus(0)

i2cbus.write_byte(ADC_ADDR,CFG_WORD)

while(1):
	time.sleep(0.1)
	adcword = i2cbus.read_word_data(ADC_ADDR,CFG_WORD)
	rawweight = (adcword & 0xff)*0x100+(adcword & 0xff00)/0x100
	if (rawweight>32767):
		rawweight -= 65536
	print(rawweight)
