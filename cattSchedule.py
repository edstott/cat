import threading
import time,datetime,calendar
import Queue
import re
import logging

import cattEvent

T_FMT = '%a, %d %b %Y %H:%M:%S'

class cattSchedule(threading.Thread):

	cron_RE = re.compile('(?P<minute>\*|[0-5]?\d)\s\
(?P<hour>\*|[01]?\d|2[0-3])\s\
(?P<dom>\*|0?[1-9]|[12]\d|3[01])\s\
(?P<month>\*|0?[1-9]|1[0-2])\s\
(?P<dow>\*|[1-7])\s\
(?P<cmd>.*)')


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
			#print "Next event "+nextEvent.type+" is at " + time.strftime(T_FMT,time.gmtime(nextTime))
			if time.time() >= nextTime:
				#print "Executing event at " + time.strftime(T_FMT,time.gmtime())
				self.outqueue.put(nextEvent)
			#Otherwise sleep until the right time or a reschedule, then try again flag			
			else:
				self.schQueue.put((nextTime,nextEvent))
				self.resched.wait(nextTime-time.time())
				self.resched.clear()

	def addEvent(self,event):
		self.schQueue.put((event.time,event))
		logging.debug("Scheduled event "+event.type+" for " + time.strftime(T_FMT,time.gmtime(event.time)))
		self.resched.set()

	#Add an event without prompting the scheduler
	def addEventQuietly(self,event):
		self.schQueue.put((event.time,event))
		logging.debug("Scheduled event "+event.type+" for " + time.strftime(T_FMT,time.gmtime(event.time)))

	def addFeedEvent(self,eventTime,amount):
		event = cattEvent.cattEvent(cattEvent.FEED,amount,eventTime)
		self.addEvent(eventTime,event)

	def readSchedule(self,filename):
		#Format min hr dom mon dow cmd
		t = time.localtime()
		ecount = 0
		with open(filename) as f:
			for line in f:
				m = cattSchedule.cron_RE.match(line)
				if m:
					md = m.groupdict()
					#Is the day right?
					dom_ok = md['dom'] == '*' or int(md['dom']) == t.tm_mday
					#Is the month right?
					mon_ok = md['month'] == '*' or int(md['month']) == t.tm_mon
					#Is the weekday right?
					wday_ok = md['dow'] == '*' or int(md['wday']) == t.tm_wday-1
					if dom_ok and mon_ok and wday_ok:
						#Loop over hours
						for h in xrange(t.tm_hour,24):
							if md['hour'] == '*' or int(md['hour']) == h:
								#Loop over minutes
								for m in xrange(60):
									if md['minute'] == '*' or int(md['minute']) == m:
										eventTime = (t.tm_year,t.tm_mon,t.tm_mday,h,m,0,t.tm_wday,t.tm_yday,-1)
										eventCmd = md['cmd'].split(' ')
										if len(eventCmd)>1:
											event = cattEvent.cattEvent(eventCmd[0],float(eventCmd[1]),time.mktime(eventTime))
										else:
											event = cattEvent.cattEvent(eventCmd[0],time=time.mktime(eventTime))
										self.addEventQuietly(event)
										ecount += 1
				else:
					print "Bad line in "+filename
					print line
			
		#Set reschedule flag to force check for new events		
		self.resched.set()
		logging.info(str(ecount)+" events queued for today from schedule file")



def clearSchedule(self):
	try:
		while True:
			self.schQueue.get_nowait()
	except Queue.Empty:
			pass


					
