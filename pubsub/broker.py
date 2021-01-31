# Sample code for CS6381
# Vanderbilt University
# Instructor: Aniruddha Gokhale

import sys
import time
import zmq    # this package must be imported for ZMQ to work
import threading

REQUEST_TIMEOUT = 5000
REQUEST_RETRIES = 3
SUBSCRIBER_ENDPOINT = "tcp://localhost:5556"

sockpool = []

class Broker:
    def __init__(self):
        self.context = zmq.Context ()   # returns a singleton object
        self.incoming_socket = self.context.socket (zmq.REP)
        self.incoming_socket.bind ("tcp://*:5555")

    #Application interface --> run() encloses basic functionality
    def run(self):
        self.listen_publisher() # will then call notify subscriber

    def listen_publisher(self):
        while True:
            #  Wait for next request from client
            self.message = self.incoming_socket.recv_string()
            print("Received request: %s" % self.message)

            self.notify_subscriber()

    def notify_subscriber(self):
            kwargs = dict()
            kwargs['message'] = self.message
            kwargs['attempts'] = 3
            kwargs['subscriber_endpoint'] = SUBSCRIBER_ENDPOINT
            kwargs['request_timeout'] = REQUEST_TIMEOUT
            kwargs['request_retries'] = REQUEST_RETRIES
            thread = threading.Thread(target=self.lazypirate, kwargs=kwargs)
            thread.start()
            self.incoming_socket.send_string(self.message)
            #time.sleep(1)

    def lazypirate(self, subscriber_endpoint=None, message=None,
                            attempts=None, request_timeout=None, request_retries=None):
        for i in range(attempts):
            #create outbound socket to subscriber endpoint
            self.outbound_socket = self.context.socket(zmq.REQ)
            self.outbound_socket.connect(subscriber_endpoint)
            self.outbound_socket.send_string(message)
            errors = 0

            #lazy pirate to avoid port issues
            retries_left = request_retries
            while True:
                try:
                    poll_timeout = self.outbound_socket.poll(timeout)
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
                    reply = self.outbound_socket.recv_string()
                    if reply == self.message:
                        print("Server replied ok")
                        sys.exit()
                    else:
                        print("Polling error > Return Value Incorrect")

                retries_left -= 1
                print("No response from server")
                self.outbound_socket.setsockopt(zmq.LINGER, 0)
                outbound_socket.close()
                if retries_left == 0:
                    print("Exiting")
                    sys.exit()

                outbound_socket = context.socket (zmq.REQ)
                outbound_socket.connect(subscriber_endpoint)
                outbound_socket.send_string(self.message)