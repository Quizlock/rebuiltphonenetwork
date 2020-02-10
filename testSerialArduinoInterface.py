import serial

ser = serial.Serial('/dev/ttyACM0', 9600) 

print('Begining Input')

while True:
	serial_input = ser.readline()
	print(serial_input)


