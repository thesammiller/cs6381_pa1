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

from pubsub import ipaddr


REQUEST_TIMEOUT = 5000
REQUEST_RETRIES = 3
SERVER_ENDPOINT = "tcp://{}"

BABY_BROKER_ADDRESS = "10.0.0.2:5555"
#BABY_BROKER_ADDRESS = "localhost:5555"
class BabyPublisher:

    def __init__(self, topic):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.request_retries = REQUEST_RETRIES
        self.connect_str = SERVER_ENDPOINT.format(BABY_BROKER_ADDRESS)
        self.socket.connect(self.connect_str)
        self.ipaddress = list(ipaddr.local_ip4_addr_list())[0]
        self.role = "PUB"
        self.topic = topic
        self.registry = []
        self.message = ""
        

    def register_pub(self):
        print("Registering publisher")
        self.hello_message = "{role} {topic} {ipaddr}".format(role=self.role, topic=self.topic, ipaddr=self.ipaddress)
        self.reply = self.publish_lazy(self.hello_message)
        if self.reply != "none":
            self.registry = self.reply.split()
            print("Received registry.")
            
        
    def publish(self, data):
        for ipaddr in self.registry:
            self.socket = self.context.socket(zmq.REQ)
            self.connect_str = SERVER_ENDPOINT.format(ipaddr)
            self.socket.connect(self.connect_str)
            self.message = "{topic} {data}".format(topic=self.topic, data=data)
            reply = self.publish_lazy(self.message)
            if reply != "none":
                continue
            else:
                print("Error -> reply not as expected")
                break
                

    # lazy pirate to avoid port issues
    def publish_lazy(self, message):
        self.socket.send_string(message)
        self.retries_left = self.request_retries
        while True:
            #print("Socket poll and zmq pollin")
            if (self.socket.poll(REQUEST_TIMEOUT) & zmq.POLLIN) != 0:
                print("Getting reply...")
                reply = self.socket.recv_string()
                return reply


            self.retries_left -= 1
            print("No response from server")
            self.socket.setsockopt(zmq.LINGER, 0)
            self.socket.close()
            if self.retries_left == 0:
                print("Exiting")
                return "none"

            self.socket = self.context.socket(zmq.REQ)
            self.socket.connect(self.connect_str)
            self.socket.send_string(message)

