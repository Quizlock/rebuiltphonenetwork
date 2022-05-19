from gpiozero import Button
from pad4pi import rpi_gpio
import board, busio, adafruit_drv2605
from phonenetwork import PhoneNetwork

from udpcaller import UDPCaller
from udpreceiver import UDPReceiver

import pyaudio, wave
import time

##########################
#PIN CONSTANTS
##########################
#Touchtone Keypad Pins

PIN_T = [11, 9, 27, 17, 1, 7, 8, 25]
PIN_ON_HOOK = 24
PIN_OFF_HOOK = 23
PIN_MOTOR_IN = 18
PIN_MOTOR_SCL = 3
PIN_MOTOR_SDA = 2

##########################
#INITIALIZE WAVE FILES
##########################
print("Loading Wave Files...", end="")
dialtone = wave.open("./sounds/dialtone.wav", "rb")
busytone = wave.open("./sounds/busytone.wav", "rb")
ringtone = wave.open("./sounds/ringtone.wav", "rb")

startone = wave.open("./sounds/star.wav", "rb")
poundtone = wave.open("./sounds/pound.wav", "rb")

tones = []
for i in range(10):
    tones.append(wave.open("./sounds/" +str(i) + ".wav", "rb"))

##########################
#INITIALIZE GLOBAL CONTROL VARIABLES
##########################
audio_control = pyaudio.PyAudio()
#All wave files are normalized to same parameters - using dialtone as default
CHUNK_SIZE = 10*1024
BUFFER_SIZE = 65536
AUDIO_FORMAT = audio_control.get_format_from_width(dialtone.getsampwidth())
CHANNELS = dialtone.getnchannels()
RATE = dialtone.getframerate()

class KeySwitch:
    def __init__(self):
        self.pressed = False
        self.wavefile = None
        self.rewind = False
        self.phone_on_hook = True
        self.incoming_call = False

play_tone = KeySwitch()

class KeyString:
    def __init__(self):
        self.keys_pressed = ""

key_string = KeyString()

##########################
#INITIALIZE SOUND INPUT/OUTPUT
##########################

def callback(in_data, frame_count, time_info, status):
    if play_tone.wavefile and not play_tone.phone_on_hook and not play_tone.incoming_call:
        data = play_tone.wavefile.readframes(frame_count)
        if len(data) < CHUNK_SIZE: 
            print("Sending rewind message")
            play_tone.rewind = True
    else:
        data = None
    return (data, pyaudio.paContinue)

dialing_stream = audio_control.open(format=AUDIO_FORMAT, channels=CHANNELS, rate=RATE, output=True, stream_callback=callback, frames_per_buffer=CHUNK_SIZE)

##########################
#INITIALIZE PHONE HOOK
#########################
print("Initializing phone hook button...", end="")
off_hook_button = Button(PIN_OFF_HOOK) #off hook button is closed when the phone is off the hook
on_hook_button = Button(PIN_ON_HOOK) #on hook button is closed when the phone is on the hook


#Testing off_hook only - if bad try on_hook button
def hook_off():
    #Phone is off hook event
    print("Phone is off the hook now!")
    play_tone.phone_on_hook = False
    if play_tone.incoming_call:
        #Answer the incoming call
        pass
    else:
        #If no incoming call, you want to dial out - play dial tone and wait for buttons
        dialing_stream.stop_stream()
        play_tone.wavefile = dialtone
        play_tone.wavefile.rewind()
        dialing_stream.start_stream()

def hook_on(): 
    #Phone is on hook event
    print("Phone is on the hook now!")
    play_tone.phone_on_hook = True
    key_string.keys_pressed = ""
    dialing_stream.stop_stream()

on_hook_button.when_pressed = hook_on
on_hook_button.when_released = hook_off
#off_hook_button.when_pressed = hook_off

#Check default value
if off_hook_button.is_pressed and not on_hook_button.is_pressed:
    play_tone.phone_on_hook = False
elif not off_hook_button.is_pressed and on_hook_button.is_pressed:
    play_tone.phone_on_hook = True

print("Done.")

##########################
#INITIALIZE KEYPAD
##########################
#TODO: Test keypad clicks - missing keys
print("Initializing Keypad...", end="")
KEYPAD = [ [1,2,3], [4,5,6], [7,8,9], ["*",0,"#"]]
ROW_PINS = [PIN_T[3], PIN_T[2], PIN_T[1], PIN_T[0]]
COL_PINS = [PIN_T[4], PIN_T[5], PIN_T[6]]

factory = rpi_gpio.KeypadFactory()
keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)

def key_pressed(key):
    #Play the accompaning sound
    print("Pressed: ", key, end=" ")
    
    if play_tone.pressed == False:
        play_tone.pressed = True
        if key == "*":
            play_tone.wavefile = startone
        elif key == "#":
            play_tone.wavefile = poundtone
        else:
            play_tone.wavefile = tones[int(key)]

    #Update key_string
    key_string.keys_pressed = key_string.keys_pressed + str(key)
    print("Current key_string: ", key_string.keys_pressed)


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
network = PhoneNetwork("phone.conf", 4)
print("Done.")
network.print_ip_table()

#receiver = UDPReceiver(network.port)
#caller = None

#Make sure that the phone starts on the hook when loaded
if not play_tone.phone_on_hook:
    print("To complete initialization, hang up the phone.", flush=True) 

while not play_tone.phone_on_hook:
    pass


print("Entering main loop")
############################
#MAIN CONTROL LOOP
############################
while True:
    try:
        #Check for status
        if play_tone.phone_on_hook:
            #Close all open lines when phone is on the hook
        
            #Listen for calls
            #If incoming call, ring
            pass
        else:
            #Play dial tone
            if dialing_stream.is_active():
                time.sleep(0.01)
            elif play_tone.wavefile:
                print("Rewinding dialing stream")
                play_tone.rewind = False
                dialing_stream.stop_stream()
                play_tone.wavefile.rewind()
                if play_tone.wavefile != dialtone:
                    play_tone.pressed = False
                    play_tone.wavefile = None
                dialing_stream.start_stream()
            #When dial is valid, connect to other phone
            #Analyze key string
            if network.room_number_in_ip_table(key_string.keys_pressed):
                #Call room 
                #caller = UDPCaller(network.get_room_ip, network.port)
                print("Calling " + key_string.keys_pressed)
    except Exception as e:
        print(e)
        break 


############################
#CLOSE OUT FILES
############################
dialing_stream.stop_stream()
dialing_stream.close()
dialtone.close()
busytone.close()
ringtone.close()

startone.close()
poundtone.close()
for i in range(10):
    tones[i].close()

audio_control.terminate()
