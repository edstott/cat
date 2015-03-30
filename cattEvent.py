import time

class cattEvent:
	
	def __init__(self,*args):
		self.type = args[0]
		self.time = time.localtime()
		try:
			self.data = args[1]
		except IndexError:
			pass
