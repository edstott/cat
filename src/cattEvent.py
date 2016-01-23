import time

READ_SCHEDULE = 'READ_SCHEDULE'
TEST = 'TEST'
FEED = 'FEED'
WEIGHT_CHANGE = 'WEIGHT_CHANGE'
DELIVERED = 'DELIVERED'
FEED_ERROR = 'FEED_ERROR'
UPDATE_WEB = 'UPDATE_WEB'
UPDATE_STAT = 'UPDATE_STAT'
SENT_TWEET = 'SENT_TWEET'
KILL = 'KILL'

class cattEvent:
	
	def __init__(self,etype,data = None,time = time.time()):
		self.type = etype
		self.time = time
		self.data = data
		#try:
	#		self.data = args[1]
	#	except IndexError:
	#		pass

	def string(self):
		string = self.type
		if self.data:
			string += ' '+str(self.data)
		return string

	def isfeedEvent(self):
		return self.type == FEED

	def iswebEvent(self):
		return self.type == UPDATE_WEB

def feedEvent(amount,time = time.time()):
	return cattEvent(FEED,data = amount,time = time)

def webEvent(time=time.time()):
	return cattEvent(UPDATE_WEB,time = time)


