import RPIO
import cattEvent

#Parameters
PID_GPIO = 21
PID_REARM = 60000
#PID_REARM = 5000

class PIR:

	def __init__(self):
		#Setup PIR interrupt
		RPIO.add_interrupt_callback(PID_GPIO,self.callback,edge="rising",debounce_timeout_ms=PID_REARM,threaded_callback=True)

	def callback(self,gpio_id,val):
		self.eventQueue.put_nowait(cattEvent.cattEvent("PIR"))

	def enableCallback(self,eventQueue):
		self.eventQueue = eventQueue
		RPIO.wait_for_interrupts(threaded=True)

	def __del__(self):
		RPIO.cleanup()

