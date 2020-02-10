from gpiozero import Button
import serial

def print_phone_number(number):
	if len(number) == 10:
		print('Calling telephone number: ')
		print('{} - {} - {}'.format(number[0:3], number[3:6], number[6:]))
	else:
		print(number) 

def main():
	#Initialize main working variables
	receiving_call = False
	current_number = ''

	print('Initializing Rotary Phone...')

	#Handset switch is input to GPIO15 - pulled HIGH
	switch = Button(15)
	print ('Switch connected.')

	#TODO: Connect the microphone and the headset
	

	#Connect to the arduino controlling the rotary dial
	dial_connection = serial.Serial('/dev/ttyACM0', 9600)

	#Main Loop	
	while True:

		#TODO: Check for incoming call
	
		#Don't really do anything until you take the reciever off the hook. 
		if switch.is_pressed and receiving_call == False:
			#Will wait for 10 digits or switch to be closed
			digit_count = 0

			print('Waiting for dials ...')

			# dial_connection.flush()
			while switch.is_pressed and digit_count < 10:
				#read the next digit
				input_digit = dial_connection.readline()
				#TODO: sanitize the input
				
				#add the new digit to the others
				current_number += input_digit.decode('utf-8').rstrip()	
				digit_count += 1
				print(digit_count, end='', flush=True)
		
			print('')		
			print_phone_number(current_number)
			current_number = ''	


if  __name__ == '__main__':
	main()
