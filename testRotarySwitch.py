from gpiozero import LED, Button
from signal import pause

rotarySwitch = Button(15)
signalLed = LED(18)

rotarySwitch.when_pressed = signalLed.on
rotarySwitch.when_released = signalLed.off

pause()
