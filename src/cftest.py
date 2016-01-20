import cattFeeder
import cattEvent
import cattSchedule
import time
import Queue

try:
	#CF = cattFeeder.cattFeeder()
	inqueue = Queue.Queue()
	CS = cattSchedule.cattSchedule(inqueue)

	time.sleep(3.0)
	CS.readSchedule('sched.txt')
	#CS.addFeedEvent(time.time()+10,5.0)
	#time.sleep(5.0)
	#CS.addFeedEvent(time.time()+1,5.0)

	time.sleep(600.0)
except KeyboardInterrupt:
	#CF.kill()
	#CF.join()
	pass
