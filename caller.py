import socket
import threading 
import pyaudio

class Caller:
    def __init__(self, ip_address, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.sock.connect((ip_address, port))

        except:
            print('Could not connect to server: ' + str(ip_address) + ":" + str(port))
            self.sock.close()

        chunk_size = 1024
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 20000

        #Mic Init
        self.p_aud = pyaudio.PyAudio()

        self.playing_stream = self.p_aud.open(format=audio_format, channels=channels, rate=rate, output=True, frames_per_buffer=chunk_size)
        self.recording_stream = self.p_aud.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk_size)

        print('Connected to other phone')

        #start threads
        recieve_thread = threading.Thread(target=self.receive_data).start()
        self.send_data()

    def receive_data(self):
        while True:
            try:
                data = self.sock.recv(1024)
                self.playing_stream.write(data)
            except:
                pass


    def send_data(self):
        while True:
            try:
                data = self.recording_stream.read(1024)
                self.sock.sendall(data)
            except:
                pass
