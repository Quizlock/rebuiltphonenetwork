import threading
import time

class IncomingCallHandler:

    def __init__(self):
        self.incoming_call = False

def new_thread(callhandler):
    print("Open thread")
    time.sleep(5)
    callhandler.incoming_call = True
    time.sleep(5)
    print("Close thread")

def main():
    print("Beginning Thread Test")
    call_handler = IncomingCallHandler()
    my_thread_1 = threading.Thread(target=new_thread, args=(call_handler,))
    my_thread_1.start()

    print("Testing....")
    while True:
        if call_handler.incoming_call:
            print("Hooray!")
            break


if __name__ == "__main__":
    main()
