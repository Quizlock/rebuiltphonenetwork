
import configparser

class PhoneNetwork:

    def __init__(self, config_file, self_address):
        config = configparser.ConfigParser()
    
        config.read(config_file)

        self.port = int(config['DEFAULT']['Port'])
        self.ip_table = {'0':'null', '1':'127.0.0.1'} #Ip Table Entries 0 and 1 are blank. Rooms 2 - 8 are reserved for Room Numbers 
        for i in range(2, 8):
            room_name = "Room" + str(i)
            if room_name in config['DEFAULT']:
                self.ip_table[str(i)] = config['DEFAULT'][room_name]

        self.my_room_number = self_address # Room Number of the Phone

    def room_number_in_ip_table(self, room_number):
        return room_number in self.ip_table

    def get_room_ip(self, room_number):
        return self.ip_table[room_number]

    def print_ip_table(self):
        print("-----CURRENT PHONE NETWORK-----")
        for num,ip in self.ip_table.items():
            print(num, end="")
            print(": ", end="")
            print(ip, end="")
            if int(num) == self.my_room_number:
                print(" <------ CURRENT PHONE")
            else:
                print("")
