import socket
import threading 
import pyaudio
import sys

class Caller:
    def __init__(self, ip_address, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            print('Attempting to connect to ' + str(ip_address) + ":" + str(port))
            self.sock.connect((ip_address, port))
            opened_socket = True

        except socket.error as msg:
            print('Could not connect to server: ' + str(ip_address) + ":" + str(port))
            print('Error code' + str(msg))
            self.sock.close()
            opened_socket = False

        if opened_socket:
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
            send_thread = threading.Thread(target=self.send_data).start()

    def receive_data(self):
        while True:
            try:
                data = self.sock.recv(1024)
                self.playing_stream.write(data, exception_on_underflow=False)
            except:
                pass


    def send_data(self):
        while True:
            try:
                data = self.recording_stream.read(1024, False)
                self.sock.sendall(data)
            except:
                pass
