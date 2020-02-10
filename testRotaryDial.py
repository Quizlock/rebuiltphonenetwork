from gpiozero import Button
from datetime import datetime
from signal import pause

pin = 14

rotarySwitch = Button(pin, pull_up = True, bounce_time =0.1)

readingNumber = False
rotatorTime = 100

print('Ready to go!')

# wait for the first release
rotarySwitch.wait_for_release()

readingNumber = True
print('Tick 1: Starting measure')

# after the first release, count the number of subsequent
i = 2
while readingNumber:
	timeStart = datetime.now()
	rotarySwitch.wait_for_release()
	timeEnd = datetime.now()
	timeDelta = timeEnd - timeStart
	print(timeDelta.microseconds)
		
	if i > 100:
		readingNumber = False
	i = i + 1 	

