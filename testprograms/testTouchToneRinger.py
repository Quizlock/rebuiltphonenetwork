import board
import busio
import adafruit_drv2605

i2c = busio.I2C(3, 2)
drv = adafruit_drv2605.DRV2605(i2c)

while True:
    input_val = input("Enter effect to play (1-123, x to quit):")

    if input_val == "x":
        exit()

    if int(input_val) >= 1 and int(input_val) <= 123:
        drv.sequence[0] = adafruit_drv2605.Effect(int(input_val))

        for i in range(1, 7):
            drv.sequence[i] = drv.sequence[0]

        drv.play()

    else: 
        print("Invalid input!")
