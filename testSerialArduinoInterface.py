import serial

ser = serial.Serial('/dev/ttyUSB0', 9600) 

print('Begining Input')

while True:
	serial_input = ser.readline()
	print(serial_input)


