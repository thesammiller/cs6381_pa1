# Sample code for CS6381
# Vanderbilt University
# Instructor: Aniruddha Gokhale

import sys
import time
import zmq    # this package must be imported for ZMQ to work
import threading
from collections import defaultdict

REQUEST_TIMEOUT = 5000
REQUEST_RETRIES = 3

IPADDRESS = "localhost"

class BabyBroker:
    def __init__(self):
        print("initializing baby broker API")
        self.context = zmq.Context ()   # returns a singleton object
        self.incoming_socket = self.context.socket(zmq.REP)
        #creating a server bound to port 5555
        self.incoming_socket.bind("tcp://*:5555}")
        self.registry = {}
        self.registry["PUB"] = defaultdict(list)
        self.registry["SUB"] = defaultdict(list)

    #Application interface --> run() encloses basic functionality
    def run(self):
        while True:
            print("Listening...")
            self.listen()

    def listen(self):
        #  Wait for next request from client
        self.message = self.incoming_socket.recv_string()
        print(self.message)
        role, topic, ipaddr = self.message.split()
        print("Received request: Role -> {role}\t\tTopic -> {topic}\t\tData -> {data}".format(role=role, topic=topic, data=ipaddr))
        if ipaddr not in self.registry[role][topic]:
            self.registry[role][topic].append(ipaddr)

        #based on our role, we need to find the companion ip addresses in the registry
        if role == "PUB":
            other = "SUB"
        if role == "SUB":
            other = "PUB"

        #if we have entries in the registry for the companion ip addresses
        if self.registry[other] != []:
            #registry[other][topic] is a list of ip addresses
            #these belong to the companion to the registering entity
            result = " ".join(self.registry[other][topic])

        #we'll have to check for nones in sub and pub
        else:
            result = "none"

        self.incoming_socket.send_string(result)

        