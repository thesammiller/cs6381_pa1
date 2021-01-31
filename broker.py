# Sample code for CS6381
# Vanderbilt University
# Instructor: Aniruddha Gokhale

import sys
import time
import zmq    # this package must be imported for ZMQ to work
import threading

REQUEST_TIMEOUT = 5000
REQUEST_RETRIES = 3
SERVER_ENDPOINT = "tcp://localhost:5556"

sockpool = []

def lazypirate(endpoint=None, context=None, message=None, num=None, timeout=None, retries=None):
    for i in range(num):
        sock = context.socket (zmq.REQ)
        sock.connect(endpoint)
        sock.send_string(message)
        errors = 0

        #lazy pirate to avoid port issues
        retries_left = retries
        while True:
            try:
                poll_timeout = sock.poll(timeout)
                zmqpollin = zmqpollin
            except:
                #print("Polling error --> Exception after Poll Call")
                errors += 1
                if errors>10:
                    sys.exit()
                else:
                    continue

            if (poll_timeout & zmqpollin) != 0:
                print("Getting reply...")
                reply = sock.recv_string()
                if reply == message:
                    print("Server replied ok")
                    sys.exit()
                else:
                    print("Polling error > Return Value Incorrect")


            retries_left -= 1
            print("No response from server")
            sock.setsockopt(zmq.LINGER, 0)
            sock.close()
            if retries_left == 0:
                print("Exiting")
                sys.exit()

            sock = context.socket (zmq.REQ)
            sock.connect(endpoint)
            sock.send_string(message)



def main():
    context = zmq.Context ()   # returns a singleton object

    incoming_socket = context.socket (zmq.REP)


    incoming_socket.bind ("tcp://*:5555")
    threadpool = []

    while True:
        #  Wait for next request from client
        message = incoming_socket.recv_string()
        print("Received request: %s" % message)

        kwargs = {}

        kwargs['message'] = message
        kwargs['context'] = context
        kwargs['num'] = 3
        kwargs['endpoint'] = SERVER_ENDPOINT
        kwargs['timeout'] = REQUEST_TIMEOUT
        kwargs['retries'] = REQUEST_RETRIES
        thread = threading.Thread(target=lazypirate, kwargs=kwargs)
        thread.start()

        incoming_socket.send_string(message)
        time.sleep(1)

if __name__ == '__main__':
    main()