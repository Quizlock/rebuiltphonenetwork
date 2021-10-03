import serial
import socket
import threading
import pyaudio
import caller

ser = serial.Serial('/dev/ttyUSB0', 9600) 

print('Reading Phone Input')

while True:
    serial_input = ser.read().decode()
    if serial_input == "-":
        #Begin Call 
        print('Begining Phone Call')
    elif serial_input == "o":
        #End Call
        print('Ending Phone Call')
    elif serial_input == "0":
        #Call Operator
        print('Calling Operator')
    elif serial_input == "1":
        #Call Phone
        print('Calling Outside Line')
    else: 
        #Call Room
        room_number = int(serial_input)
        print('Calling Room Number ' + str(room_number))
        caller_device = caller.Caller("10.0.0.1", 6666)
