import pprint

from googlevoice import Voice

def run():
	
	voice = Voice()

	voice.login()

	pprint.pprint(voice.Settings)

if __name__ == '__main__':
	run()
