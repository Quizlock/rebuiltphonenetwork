import socket 
import threading
import pyaudio
import queue
import time

class UDPReceiver:

    def __init__(self, port):
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = port
        self.CHUNK_SIZE = 10*1024
        self.BUFFER_SIZE = 65536
        AUDIO_FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100

        self.input_queue = queue.Queue(maxsize=2000)

        self.p_aud = pyaudio.PyAudio()
        self.playing_stream = self.p_aud.open(format=AUDIO_FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=self.CHUNK_SIZE)
        self.recording_stream = self.p_aud.open(format=AUDIO_FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=self.CHUNK_SIZE)


    def open_listener(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF,self.BUFFER_SIZE)
            self.sock.bind(('', self.port))
            self.open_socket = True
        except:
            print('Could not bind to port ' + str(self.port))
            self.open_socket = False


    def accept_connections(self):
        print('Running on ' + str(self.ip) + ":" + str(self.port))

        message, client_address = self.sock.recvfrom(self.BUFFER_SIZE)
        print('Receiving connection from ', client_address, message)

        self.sending_thread = threading.Thread(target=self.send_data,args=(client_address,))
        self.receiving_thread = threading.Thread(target=self.receive_data,args=())

        self.sending_thread.start()
        self.receiving_thread.start()


    def receive_data(self):
        def get_audio_data():
            while self.open_socket:
                frame, client_address = self.sock.recvfrom(self.BUFFER_SIZE)
                self.input_queue.put(frame)
                print('Queue size...',self.input_queue.qsize())

        listener_thread = threading.Thread(target=get_audio_data, args=())
        listener_thread.start()

        while self.open_socket:
            try:
                frame = self.input_queue.get()
                self.playing_stream.write(frame)
            except Exception as msg:
                print(msg)


    def send_data(self, address):
        while self.open_socket:
            data = self.recording_stream.read(self.CHUNK_SIZE)
            self.sock.sendto(data, address)
            time.sleep(0.001)

    def pause(self):
        self.sock.close()
        self.open_socket = False
        self.playing_stream.stop_stream()
        self.recording_stream.stop_stream()
    
    def start_streams(self):
        if not self.open_socket:
            open_listener()
        self.playing_stream.start_stream()
        self.recording_stream.start_stream()
        self.accept_connections()
