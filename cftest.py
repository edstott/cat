import cattFeeder
import cattEvent
import time

CF = cattFeeder.cattFeeder()

time.sleep(5.0)
print "Feed"
CF.inqueue.put(cattEvent.cattEvent("deliver",20.0))
time.sleep(5.0)
