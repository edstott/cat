import cattFeeder
import cattEvent
import cattSchedule
import time

try:
	CF = cattFeeder.cattFeeder()
	CS = cattSchedule.cattSchedule(CF.inqueue)

	time.sleep(10.0)
	CS.addFeedEvent(time.time()+10,5.0)
	time.sleep(5.0)
	CS.addFeedEvent(time.time()+1,5.0)

	time.sleep(600.0)
except KeyboardInterrupt:
	CF.kill()
	CF.join()
