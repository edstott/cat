import RPIO
import cattEvent
import time

#Parameters
PID_GPIO = 22
PID_REARM = 1000
#PID_REARM = 5000
TRIGGER_WIN = 5.0 #Length of trigger window
TRIGGER_COUNT = 2 #Number of edges required for trigger

class PIR:

	def __init__(self):
		#Setup PIR interrupt
		RPIO.add_interrupt_callback(PID_GPIO,self.callback,edge="rising",debounce_timeout_ms=PID_REARM,threaded_callback=True)
		self.lastEdgeTime = 0
		self.triggerCount = 0

	def callback(self,gpio_id,val):
		if time.time() < self.lastEdgeTime + TRIGGER_WIN:
			self.triggerCount += 1
			if self.triggerCount == TRIGGER_COUNT:
				self.eventQueue.put_nowait(cattEvent.PIREvent())
		else:
			self.lastEdgeTime = time.time()
			self.triggerCount = 1

	def enableCallback(self,eventQueue):
		self.eventQueue = eventQueue
		RPIO.wait_for_interrupts(threaded=True)

	def __del__(self):
		RPIO.cleanup()

