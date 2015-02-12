import time

class cattEvent:
	
	def __init__(self,*args):
		self.type = args[0]
		self.time = args[1]
		try:
			self.data = args[2]
		except:
			pass
