import pyaudio
import wave
import sys
import time
from gpiozero import Button

CHUNK = 1024

dialtone = wave.open("dialtone.wav", 'rb')
tone0 = wave.open("busytone.wav", 'rb')

switch = Button(24)
class OnOff:
    def __init__(self):
        self.pressed = False

play_tone = OnOff()
def pressed_trigger():
    play_tone.pressed = True

switch.when_pressed = pressed_trigger

wf = dialtone
pa = pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    if play_tone.pressed:
        data = tone0.readframes(frame_count)
    else:
        data = dialtone.readframes(frame_count)
    return (data, pyaudio.paContinue)

stream = pa.open(format=pa.get_format_from_width(wf.getsampwidth()), channels=wf.getnchannels(), rate=wf.getframerate(), output=True, stream_callback=callback)

stream.start_stream()


while True:
    if stream.is_active():
        time.sleep(0.01) 
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
