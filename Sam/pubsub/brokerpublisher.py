# Sample code for CS6381
# Vanderbilt University
# Instructor: Aniruddha Gokhale
#
# Code taken from ZeroMQ examples with additional
# comments or extra statements added to make the code
# more self-explanatory  or tweak it for our purposes
#
# We are executing these samples on a Mininet-emulated environment
#
#
#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#
# Added more comments

import sys

import zmq
import time

REQUEST_TIMEOUT = 5000
REQUEST_RETRIES = 3
SERVER_ENDPOINT = "tcp://localhost:5555"

class BrokerPublisher:

    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.request_retries = REQUEST_RETRIES
        self.srv_addr = "localhost"
        self.connect_str = "tcp://" + self.srv_addr + ":5555"
        self.socket.connect(self.connect_str)

    def publish(self, topic, data):
            self.message = "{topic} {data}".format(topic=topic, data=data)
            self.publish_lazy(self.message)

    # lazy pirate to avoid port issues
    def publish_lazy(self, message):
        self.socket.send_string(message)
        self.retries_left = self.request_retries
        while True:
            #print("Socket poll and zmq pollin")
            if (self.socket.poll(REQUEST_TIMEOUT) & zmq.POLLIN) != 0:
                print("Getting reply...")
                reply = self.socket.recv_string()
                if reply == self.message:
                    print("Server replied ok")
                    break
                else:
                    print("Polling error")
                    continue

            self.retries_left -= 1
            print("No response from server")
            self.socket.setsockopt(zmq.LINGER, 0)
            self.socket.close()
            if self.retries_left == 0:
                print("Exiting")
                sys.exit()

            self.socket = self.context.socket(zmq.REQ)
            self.socket.connect(SERVER_ENDPOINT)
            self.socket.send_string(message)

