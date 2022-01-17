
from phonenetwork import PhoneNetwork

from udpcaller import UDPCaller
from udpreceiver import UDPReceiver

import threading
import pyaudio, wave
import time

from pynput import keyboard

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
phone_on_hook = True 
incoming_call = False
#All wave files are normalized to same parameters - using dialtone as default
CHUNK_SIZE = 10*1024
BUFFER_SIZE = 65536
SAMPLE_WIDTH = dialtone.getsampwidth()
AUDIO_FORMAT = audio_control.get_format_from_width(SAMPLE_WIDTH)
CHANNELS = dialtone.getnchannels()
RATE = dialtone.getframerate()

##########################
#INITIALIZE SOUND INPUT/OUTPUT
##########################

def callback(in_data, frame_count, time_info, status):
    if play_tone.wavefile:
        print("1")
        data = playtone.wavefile.readframes(frame_count)
    else:
        print("0")
        data = bytes(frame_count * CHANNELS * SAMPLE_WIDTH)
    return (data, pyaudio.paContinue)

dialing_stream = audio_control.open(format=AUDIO_FORMAT, channels=CHANNELS, rate=RATE, output=True, stream_callback=callback)
dialing_stream.start_stream()

##########################
#INITIALIZE KEYPAD
##########################
class KeySwitch:
    def __init__(self):
        self.pressed = False
        self.wavefile = None

play_tone = KeySwitch()

key_string = ""

def key_pressed(key):
    global phone_on_hook
    global play_tone
    global receiver
    global key_string
    global incoming_call
    print("Pressed: ", key)
    if isinstance(key, keyboard.KeyCode):
        if phone_on_hook:
            if key.char == "a": 
                print("Picked up the receiver. Press l to put it down.")
                if incoming_call:
                    #Answer a call
                    phone_on_hook = False
                    receiver.answered_phone = True
                else:
                    #Start dialing
                    play_tone.wavefile = dialtone
                    phone_on_hook = False
        else:
            #Play the accompaning sound
            if key.char == "l": 
                print("Put down the receiver. Press a to pick it up.")
                play_tone.wavefile = None
                key_string = ""
                phone_on_hook = True
            elif play_tone.pressed == False:
                play_tone.pressed = True
                if key.char == "*":
                    play_tone.wavefile = startone
                    #Update key_string
                    key_string = key_string + key.char
                elif key.char == "#":
                    play_tone.wavefile = poundtone
                    #Update key_string
                    key_string = key_string + key.char
                elif key.char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    play_tone.wavefile = tones[int(key.char)]
                    #Update key_string
                    key_string = key_string + key.char

            

key_listener = keyboard.Listener(on_press=key_pressed)
key_listener.start()

print("Done.")

###########################
#INITIALIZE PHONE NETWORK
###########################
print("Initializing Phone Network...", end="")
network = PhoneNetwork("phone.conf", 2)
print("Done.")
network.print_ip_table()

print("Initializing Receiver...", end="")

receiver = None
def receive_calls():
    receiver = UDPReceiver(network.port)

receiver_thread = threading.Thread(target=receive_calls,args=())
receiver_thread.start()
print("Done.")


############################
#MAIN CONTROL LOOP
############################
print("Main Phone Active...")
if phone_on_hook:
    print("Phone is on the hook. Press 'a' to pick up phone.")
    
while True:
    try:
        #Check for status
        if phone_on_hook:
            if receiver.is_call_waiting():
                play_tone = ringtone
                incoming_call = True
                
            #Play Ring Tone tone
            if dialing_stream.is_active():
                time.sleep(0.01)
            else:
                print("Rewinding dialing stream")
                dialing_stream.stop_stream()
                play_tone.wavefile.rewind()
                dialing_stream.start_stream()
        elif not receiver.answered_phone:
            #Play dial tone
            if dialing_stream.is_active():
                time.sleep(0.01)
            else:
                print("Rewinding dialing stream")
                dialing_stream.stop_stream()
                play_tone.wavefile.rewind()
                if play_tone.wavefile != dialtone:
                    play_tone.pressed = False
                    play_tone.wavefile = None
                dialing_stream.start_stream()
            #When dial is valid, connect to other phone
            #Analyze key string
        else:
            #Talking on the phone
            pass
    except:
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
