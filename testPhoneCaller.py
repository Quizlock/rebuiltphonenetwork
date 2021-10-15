import serial
import socket
import threading
import pyaudio
import caller
import receiver


print('Calling Room Number ')
caller_device = caller.Caller("10.0.0.25", 10666)
