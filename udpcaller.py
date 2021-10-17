import socket
import threading 
import pyaudio
import time
import sys

class udpCaller:
    def __init__(self, ip_address, port):
        self.CHUNK_SIZE = 10*1024
        self.BUFFER_SIZE = 65536
        AUDIO_FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100

        self.ip_address = ip_address
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.BUFFER_SIZE)

        try:
            print('Attempting to connect to ' + str(self.ip_address) + ":" + str(self.port))
            message = b'Hello'
            sock.sendto(message, (ip_address, port))
            opened_socket = True

        except socket.error as msg:
            print('Could not connect to server: ' + str(self.ip_address) + ":" + str(self.port))
            print('Error code' + str(msg))
            self.sock.close()
            opened_socket = False

        if opened_socket:
            #Mic Init
            self.p_aud = pyaudio.PyAudio()

            #self.playing_stream = self.p_aud.open(format=audio_format, channels=channels, rate=rate, output=True, frames_per_buffer=chunk_size)
            self.recording_stream = self.p_aud.open(format=AUDIO_FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=self.CHUNK_SIZE)

            print('Connected to other phone')

            #start threads
            self.sending_thread = threading.Thread(target=self.send_data)
            #self.receiving_thread = threading.Thread(target=self.receive_data)

            self.sending_thread.start()
            #self.receiving_thread.start()

    def receive_data(self):
        while True:
            try:
                data = self.sock.recv(512)
                self.playing_stream.write(data)
            except:
                pass


    def send_data(self):
        while True:
            data = self.recording_stream.read(self.CHUNK_SIZE)
            self.sock.sendto(data, self.ip_address)
            time.sleep(0.001)
