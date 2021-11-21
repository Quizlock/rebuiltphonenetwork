import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

pin1 = 25
pin2 = 8
pin3 = 21
pin4 = 20
pin5 = 6
pin6 = 13
pin7 = 19
pin8 = 26

pins = [pin1, pin2, pin3, pin4, pin5, pin6, pin7, pin8]
testPin = 4
testRange = [0,1,2,3,5,6,7]

GPIO.setup(pins[testPin], GPIO.OUT)
for i in testRange:
    GPIO.setup(pins[i], GPIO.IN)

print("Testing Pin ", testPin)

GPIO.output(pins[testPin], True)
while True:
    try:
        for i in testRange:
            if GPIO.input(pins[i]) == True:
                time.sleep(1)
                if GPIO.input(pins[i]) == True:
                    print("THAT'S IT!")
                    print("Pin = ", i)
                    for j in range(3):
                        time.sleep(1)
                        print(".", end="")
                    break
                else:
                    pass
    except KeyboardInterrupt:
        GPIO.cleanup()
        quit()

GPIO.cleanup()
