import threading
import time
import cattEvent
import Queue

class cattSchedule(threading.Thread):

	def __init__(self,outqueue):
		threading.Thread.__init__(self)
		self.setDaemon(True)
		self.schQueue = Queue.PriorityQueue()
		self.resched = threading.Event()
		self.outqueue = outqueue
		self.start()

	def run(self):
		while True:
			#Get the next event, block if there are none
			(nextTime,nextEvent) = self.schQueue.get()

			#If it is time for the next event, copy it to the action queue
			print "Next event is at " + str(nextTime)
			if time.time() >= nextTime:
				print "Executing event at " + str(time.time())
				self.outqueue.put(nextEvent)
			#Otherwise sleep until the right time or a reschedule, then try again flag			
			else:
				self.schQueue.put((nextTime,nextEvent))
				self.resched.wait(nextTime-time.time())
				self.resched.clear()

	def addEvent(self,time,event):
		self.schQueue.put((time,event))
		print "Scheduled event for " + str(time)
		self.resched.set()

	def addFeedEvent(self,time,amount):
		self.addEvent(time,cattEvent.cattEvent("deliver",amount))
					
