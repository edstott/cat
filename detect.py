import RPIO
import time

def gpio_callback(gpio_id, val):
	print(time.strftime("%H:%M:%S")+": Hello Cat")

RPIO.add_interrupt_callback(21,gpio_callback,edge="rising",debounce_timeout_ms=10000)

RPIO.wait_for_interrupts()
