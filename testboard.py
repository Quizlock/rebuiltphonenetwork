from gpiozero import LED
from time import sleep

white = LED(18)

i = 0

while i < 10:
	white.on()
	sleep(1)
	white.off()
	sleep(1)
	i = i + 1
