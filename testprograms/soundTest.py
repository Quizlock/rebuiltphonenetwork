import pyaudio
import wave
import sys
import time
from gpiozero import Button
from pad4pi import rpi_gpio

CHUNK = 1024

print("Loading WAVE FILES")
dialtone = wave.open("../sounds/dialtone.wav", "rb")
print("Dial Tone: ", dialtone.getnframes())
busytone = wave.open("../sounds/busytone.wav", "rb")
print("Busy Tone: ", busytone.getnframes())
ringtone = wave.open("../sounds/ringtone.wav", "rb")
print("Ring Tone: ", ringtone.getnframes())

startone = wave.open("../sounds/star.wav", "rb")
print("Star Tone: ", startone.getnframes())
poundtone = wave.open("../sounds/pound.wav", "rb")
print("Pound Tone: ", poundtone.getnframes())

tones = []
for i in range(10):
    filename = "../sounds/" + str(i) + ".wav"
    tones.append(wave.open(filename, "rb"))
    print(f"{i} Tone : {tones[i].getnframes()}")

switch = Button(24)
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
    print("Pressed ", key)
    if play_tone.pressed == False:
        play_tone.pressed = True
        if key == "*":
            play_tone.wavefile = startone
        elif key == "#":
            play_tone.wavefile = poundtone
        else:
            play_tone.wavefile = tones[int(key)]

keypad.registerKeyPressHandler(key_pressed)
print("Done.")

class OnOff:
    def __init__(self):
        self.pressed = False
        self.wavefile = dialtone

play_tone = OnOff()
def pressed_trigger():
    if play_tone.pressed == False:
        play_tone.wavefile = dialtone

switch.when_pressed = pressed_trigger

wf = dialtone
pa = pyaudio.PyAudio()

empty_wave = bytes(wf.getsampwidth()*CHUNK)

def callback(in_data, frame_count, time_info, status):
    if play_tone.wavefile:
        data = play_tone.wavefile.readframes(frame_count)
    else:
        data = empty_wave
    return (data, pyaudio.paContinue)

stream = pa.open(format=pa.get_format_from_width(wf.getsampwidth()), channels=wf.getnchannels(), rate=wf.getframerate(), output=True, stream_callback=callback)

stream.start_stream()


while True:
    if stream.is_active():
        time.sleep(0.01) 
    else:
        print("Stream ended")
        stream.stop_stream()
        play_tone.wavefile.rewind()
        if play_tone.wavefile != dialtone:
            play_tone.pressed = False
            play_tone.wavefile = None
        stream.start_stream()

stream.stop_stream()
stream.close()
dialtone.close()
busytone.close()
ringtone.close()

startone.close()
poundtone.close()

for i in range(10):
    tones[i].close()

pa.terminate()
