import time
import weigher
import sys

scales = weigher.weigher()

try:
	while(1):
		time.sleep(0.2)
		print(str(scales.getrealweight())+"  \r"),
		sys.stdout.flush()
except KeyboardInterrupt:
	pass

print
