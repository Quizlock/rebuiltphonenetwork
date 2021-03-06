import socket 
import threading
import pyaudio

class Receiver:

    def __init__(self, port):
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = port

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind(('', self.port))
            open_socket = True
        except:
            print('Could not bind to port ' + str(self.port))
            open_socket = False

        if (open_socket):
            chunk_size = 512 
            audio_format = pyaudio.paInt16
            channels = 1
            rate = 20000

            self.p_aud = pyaudio.PyAudio()
            self.playing_stream = self.p_aud.open(format=audio_format, channels=channels, rate=rate, output=True, frames_per_buffer=chunk_size)
            self.recording_stream = self.p_aud.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk_size)
            self.accept_connections()

    def accept_connections(self):
        self.sock.listen(100)

        print('Running on ' + str(self.ip) + ":" + str(self.port))

        print('Waiting for connections...')
        c, addr = self.sock.accept()
        print('Accepted connection: ' + str(c) + ", " + str(addr))
        self.sending_thread = threading.Thread(target=self.send_data,args=(c,))
        self.receiving_thread = threading.Thread(target=self.receive_data,args=(c,))

        self.sending_thread.start()
        self.receiving_thread.start()


    def receive_data(self, sock):
        while True:
            try:
                data = sock.recv(512)
                self.playing_stream.write(data)
            except:
                pass


    def send_data(self, sock):
        while True:
            try: 
                data = self.recording_stream.read(512)
                sock.sendall(data)
            except:
                pass
