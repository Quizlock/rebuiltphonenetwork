import pyaudio
import wave
import sys
import time
from gpiozero import Button
from pad4pi import rpi_gpio

CHUNK = 1024

print("Loading WAVE FILES")
dialtone = wave.open("0.wav", 'rb')
print("Dial Tone: ", dialtone.getnframes())
busytone = wave.open("busytone.wav", 'rb')
print("Busy Tone: ", busytone.getnframes())
tone0 = wave.open("dialtone.wav", 'rb')
print("0 Tone: ", tone0.getnframes())

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
        play_tone.tone = key

keypad.registerKeyPressHandler(key_pressed)
print("Done.")

class OnOff:
    def __init__(self):
        self.pressed = False
        self.tone = -1

play_tone = OnOff()
def pressed_trigger():
    if play_tone.pressed == False:
        play_tone.pressed = True
        play_tone.tone = "B"

switch.when_pressed = pressed_trigger

wf = dialtone
pa = pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    if play_tone.pressed:
        if play_tone.tone == "B":
            data = busytone.readframes(frame_count)
        else:
            data = tone0.readframes(frame_count)
    else:
        data = dialtone.readframes(frame_count)
    return (data, pyaudio.paContinue)

stream = pa.open(format=pa.get_format_from_width(wf.getsampwidth()), channels=wf.getnchannels(), rate=wf.getframerate(), output=True, stream_callback=callback)

stream.start_stream()


while True:
    if stream.is_active():
        time.sleep(0.1) 
    else:
        print("Stream ended")
        play_tone.pressed = False
        stream.stop_stream()
        dialtone.rewind()
        tone0.rewind()
        stream.start_stream()

stream.stop_stream()
stream.close()
dialtone.close()
tone0.close()

pa.terminate()
