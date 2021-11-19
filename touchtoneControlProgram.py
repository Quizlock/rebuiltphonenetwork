from gpiozero import Button
from pad4pi import rpi_gpio
import board, busio, adafruit_drv2605
from phonenetwork import PhoneNetwork

from udpcaller import UDPCaller
from udpreceiver import UDPReceiver

##########################
#INITIALIZE PHONE HOOK
#########################
print("Initializing phone hook button...", end="")
off_hook_button = Button(23) #off hook button is closed when the phone is off the hook
on_hook_button = Button(24) #on hook button is closed when the phone is on the hook
phone_on_hook = True 

def hook_switched():
    if off_hook_button.is_pressed and not on_hook_button.is_pressed:
        #Phone is off hook event
        print("Phone is off the hook now!")
        phone_on_hook = False
    elif not off_hook_button.is_pressed and on_hook_button.is_pressed:
        #Phone is on hook event
        print("Phone is on the hook now!")
        phone_on_hook = True

on_hook_button.when_pressed = hook_switched
off_hook_button.when_pressed = hook_switched

#Check default value
if off_hook_button.is_pressed and not on_hook_button.is_pressed:
    phone_on_hook = False
elif not off_hook_button.is_pressed and on_hook_button.is_pressed:
    phone_on_hook = True

print("Done.")

##########################
#INITIALIZE KEYPAD
##########################
print("Initializing Keypad...", end="")
KEYPAD = [ [1,2,3], [4,5,6], [7,8,9], ["*",0,"#"]]
ROW_PINS = [9, 11, 20, 21]
COL_PINS = [26, 19, 13]

factory = rpi_gpio.KeypadFactory()
keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)

def key_pressed(key):
    print(key)

keypad.registerKeyPressHandler(key_pressed)
print("Done.")

###########################
#INITIALIZE RINGER
###########################
print("Intializing I2C at ", board.SCL, board.SDA, end="")
print("...", end="")
i2c = busio.I2C(board.SCL, board.SDA)
drv = adafruit_drv2605.DRV2605(i2c)

drv.sequence[0] = adafruit_drv2605.Effect(1) #Strong Click - 100%
drv.sequence[1] = adafruit_drv2605.Pause(0.5) #.5 Sec Pause
drv.sequence[2] = adafruit_drv2605.Effect(47) #Buzz 1 - 100%
drv.sequence[3] = adafruit_drv2605.Effect(0) #None

print("Done.")

###########################
#INITIALIZE PHONE NETWORK
###########################
print("Initializing Phone Network...", end="")
network = PhoneNetwork("phone.conf", 2)
print("Done.")
network.print_ip_table()

receiver = UDPReceiver(network.port)

#Make sure that the phone starts on the hook when loaded
if not phone_on_hook:
    print("To complete initialization, hang up the phone", end="")
while not phone_on_hook:
    print(".", end="")

while True:
    try:
        #Check for status
        pass
    except:
        break 
