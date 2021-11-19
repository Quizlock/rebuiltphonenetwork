
import configparser

class PhoneNetwork:

	def __init__(self, config_file, self_address):
		config = configparser.ConfigParser()
	
		config.read(config_file)

		self.port = int(config['DEFAULT']['Port'])
		self.ip_table = ['null', '127.0.0.1'] #Ip Table Entries 0 and 1 are blank. Rooms 2 - 8 are reserved for Room Numbers 
		for i in range(2, 8):
			room_name = "Room" + str(i)
			if room_name in config['DEFAULT']:
				self.ip_table.insert(i, config['DEFAULT'][room_name])

		self.my_room_number = self_address # Room Number of the Phone

	def print_ip_table(self):
		print("-----CURRENT PHONE NETWORK-----")
		for i in range(len(self.ip_table)):
			print(i, end="")
			print(": ", end="")
			print(self.ip_table[i], end="")
			if i == self.my_room_number:
				print(" <------ CURRENT PHONE")
			else:
				print("")
