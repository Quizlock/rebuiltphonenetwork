import socket 
import threading
import pyaudio
import queue
import time

class udpReceiver:

    def __init__(self, port):
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = port
        self.CHUNK_SIZE = 10*1024
        self.BUFFER_SIZE = 65536
        AUDIO_FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100

        self.input_queue = queue.Queue(maxsize=2000)

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF,self.BUFFER_SIZE)
            self.sock.bind(('', self.port))
            open_socket = True
        except:
            print('Could not bind to port ' + str(self.port))
            open_socket = False

        if open_socket:
            self.p_aud = pyaudio.PyAudio()
            self.playing_stream = self.p_aud.open(format=AUDIO_FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=self.CHUNK_SIZE)
            #Just test receiving a stream first
            #self.recording_stream = self.p_aud.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk_size)
            self.accept_connections()

    def accept_connections(self):
        print('Running on ' + str(self.ip) + ":" + str(self.port))

        message, client_address = self.sock.recvfrom(self.BUFFER_SIZE)
        print('Receiving connection from ', client_address, message)

        #self.sending_thread = threading.Thread(target=self.send_data,args=(c,))
        self.receiving_thread = threading.Thread(target=self.receive_data,args=(c,))

        #self.sending_thread.start()
        self.receiving_thread.start()


    def receive_data(self, sock):
        def get_audio_data():
            while True:
                frame, client_address = sock.recvfrom(self.BUFF_SIZE)
                self.input_buffer.put(frame)
                print('Queue size...',input_buffer.qsize())

        listener_thread = threading.Thread(target=getAudioData, args=())
        listener_thread.start()

        while True:
            try:
                frame = q.get()
                self.playing_stream.write(frame)
            except:
                pass


    def send_data(self, sock):
        while True:
            try: 
                data = self.recording_stream.read(1024)
                sock.sendall(data)
            except:
                pass
