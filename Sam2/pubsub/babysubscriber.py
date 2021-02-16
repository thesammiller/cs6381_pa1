# Sample code for CS6381
# Vanderbilt University
# Instructor: Aniruddha Gokhale

import sys
import time
import zmq    # this package must be imported for ZMQ to work
import threading
from collections import defaultdict

from pubsub import ipaddr


REQUEST_TIMEOUT = 5000
REQUEST_RETRIES = 3
SERVER_ENDPOINT = "tcp://{}"

BABY_BROKER_ADDRESS = "10.0.0.2:5555"
#BABY_BROKER_ADDRESS = "localhost:5555"
SUBSCRIBER_PORT = "5556"

class BabySubscriber:
    def __init__(self, topic):
        self.context = zmq.Context ()   # returns a singleton object
        self.socket = self.context.socket (zmq.REP)
        self.socket.bind ("tcp://*:{}".format(SUBSCRIBER_PORT))
        self.topic = topic
        print("Baby Subscriber API initialized. Listening on {}".format(SUBSCRIBER_PORT))
        self.register_sub()
        

    def register_sub(self):
        print("Registering Baby Subscriber API")
        self.hello_socket = self.context.socket(zmq.REQ)
        self.hello_request_retries = REQUEST_RETRIES
        self.connect_str = "tcp://" + BABY_BROKER_ADDRESS
        self.hello_socket.connect(self.connect_str)
        self.ipaddress = list(ipaddr.local_ip4_addr_list())[0] + ":{}".format(SUBSCRIBER_PORT)
        self.role = "SUB"
        self.hello_message = "{role} {topic} {ipaddr}".format(role=self.role, topic=self.topic, ipaddr=self.ipaddress)
        print(self.hello_message)
        self.hello_socket.send_string(self.hello_message)
        self.reply = self.hello_socket.recv_string()
        if self.reply != "none":
            self.registry = self.reply.split()
        else:
            print("no publisher")
    
    def listen(self):
        print("Baby Subscriber API listening.")
        #  Wait for next request from client
        self.message = self.socket.recv_string()
        topic, *data = self.message.split()
        print("received data {data}".format(data=data))
        self.socket.send_string(self.message)
        return data
        
                
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
                    return reply
                else:
                    print("Polling error")
                    continue

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

