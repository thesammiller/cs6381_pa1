import os
import sys
import time

import zmq
from random import randrange
from collections import defaultdict

import util

PROXY_SERVER_ADDRESS_PUB = "tcp://10.0.0.1:5555"
PROXY_SERVER_ADDRESS_SUB = "tcp://10.0.0.1:5556"

BABY_PROXY_SERVER_ADDRESS = "tcp://10.0.0.2:5555"

BABY_PROXY_NO_PUBLISHERS = "NO_PUBLISHERS"

# BabyProxy listens on port :5555 for any connections
# Connecting request should prefix with "pub" or "sub"
# If pub, BabyBroker registers the address under topics
# If sub, BabyBroker sends a string of all the addresses


class BabyProxy:
    def __init__(self):
        self.context = zmq.Context ()   # returns a singleton object
        self.incoming_socket = self.context.socket (zmq.REP)
        self.incoming_socket.bind ("tcp://*:5555")
        self.publisher = defaultdict(list)

    #Application interface --> run() encloses basic functionality
    def run(self):
        while True:
            self.listener() # will then call notify subscriber

    def listener(self):
        #  Wait for next request from client
        self.message = self.incoming_socket.recv_string()
        parsemsg = self.message.split()
         #make sure that we can parse the message as expected
         # format -> "pub 10.0.0.1:5678 90210 12345"
        if len(parsemsg) > 3:
            role, address, *topics = self.message.split()
        else:
            print("Invalid number of argumetnts sent to BabyBroker")
            return
         
        #If a publisher shows up, register their address in our dictionary under the topic
        if role == "pub":
            for t in topics.split():
                print("Adding {address} to topic {topic}".format(address=address, topic=topic))
                self.publisher[topic].append(address)
            util.lazy_pirate(self.incoming_socket, "ok")

        #If a subscriber shows up, return the values of the topic dictionary
        if role == "sub":
            print("Registering sub")
            returnmsg = ""
            for addr in self.publishers[topic]:
                returnmsg += addr + " "
            returnmsg = returnmsg if returnmsg != "" else BABY_PROXY_NO_PUBLISHERS
            util.lazy_pirate(self.incoming_socket, self.returnmsg)

        return

class Proxy:
    def __init__(self):
        self.context = zmq.Context()
        self.poller = zmq.Poller()
        self.xsubsocket = self.create_XSub()
        self.xpubsocket = self.create_XPub()
        
         
    def get_context(self): 
        return self.context 

    def create_XSub(self):
        self.xsubsocket = self.context.socket(zmq.XSUB)
        self.xsubsocket.bind("tcp://*:5555")
        self.register_poller(self.xsubsocket)
        return self.xsubsocket

    def create_XPub(self):
        self.xpubsocket = self.context.socket (zmq.XPUB)
        self.xpubsocket.setsockopt(zmq.XPUB_VERBOSE, 1)
        self.xpubsocket.bind ("tcp://*:5556")
        self.register_poller(self.xpubsocket)
        return self.xpubsocket

    # unsure of parameters
    def register_poller(self, entity_id):
        self.poller.register(entity_id, zmq.POLLIN)
        return self.poller

    def poll(self):
        print ("Poll with a timeout of 1 sec")
        self.events = dict (self.poller.poll (1000))
        print ("Events received = {}".format (self.events))
        self.getPubData()
        self.getSubData()

    def getPubData(self):
        # Is there any data from publisher? Note that the proxy
        # will get only that data for which it has relayed
        # subscriptions to the publisher. Note that ZMQ in recent
        # versions is doing filtering on the publisher side. Thus,
        # not all data from publishers will even show up on proxy.
        if self.xsubsocket in self.events:
            msg = self.xsubsocket.recv_string()
            print ("Publication = {}".format (msg))
            # send the message to subscribers
            self.xpubsocket.send_string(msg)


    def getSubData(self):
    # Is there any data from subscriber? Note, this is
        # needed because we must relay the subscription info
        # to all my publishers else they will never send anything
        # to us given that we are a XSUB/XPUB entity
        if self.xpubsocket in self.events:
            msg = self.xpubsocket.recv_string()
            print("Subscription = {}".format(msg))
            # send the subscription info to publishers
            self.xsubsocket.send_string(msg)

    def run(self):
        while True:
            try:
                self.poll()
            except (NameError):
                print("Exception thrown: {}".format(sys.exc_info()[1]))

        #what to do with topic in register_pub?
        #I think we store the topic into a dictionary with the IP.
        #defaultdict is a Python collection that has an empty list
        #it avoids some exception handling/checking if key is there

class Publisher:

    def __init__(self, topic):
        self.context = zmq.Context()
        self.socket = None
        self.topic = topic

    def register_pub(self):
        self.socket = self.context.socket(zmq.PUB)
        print("Publisher connecting to proxy at: {}".format(PROXY_SERVER_ADDRESS_PUB))
        self.socket.connect(PROXY_SERVER_ADDRESS_PUB)
        

    def publish(self, value):
        #what to do with topic and val here?
        #I think that the topic for the below is zipcode
        # the value is temperature and humidity
        # so this should just take topic and value and then send them
        #to the broker
        # I think the while True loop would be in the App logic
        # something might publish constantly, but something else 
        # might only publish once or twice

        # keep publishing 
        
        #print ("Message API Sending: {} {}".format(self.topic, value))
        self.socket.send_string("{topic} {value}".format(topic=self.topic, value=value))


class Subscriber:

    def __init__(self, topic):
        self.context = zmq.Context()
        self.topic = topic

    def register_sub(self):
        # Since we are the subscriber, we use the SUB type of the socket
        self.socket = self.context.socket(zmq.SUB)

        # Here we assume publisher runs locally unless we
        # send a command line arg like 10.0.0.2
        print("Collecting updates from weather server proxy at: {}".format(PROXY_SERVER_ADDRESS_SUB))
        self.socket.connect(PROXY_SERVER_ADDRESS_SUB)        
        # any subscriber must use the SUBSCRIBE to set a subscription, i.e., tell the
        # system what it is interested in
        self.socket.setsockopt_string(zmq.SUBSCRIBE, self.topic)


    #how to process and print message in sub
    def process_msg(self):
        return self.socket.recv_string()


class FloodSubscriber:
    def __init__(self, topic):
        self.context = zmq.Context()
        self.topic = topic
        self.socket = None
        self.role = "sub"
        self.address = list(util.local_ip4_addr_list())[0]
        self.publishers = []
        print("Using IP address {}".format(self.address))

    def register_sub(self):
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(BABY_PROXY_SERVER_ADDRESS)
        #assuming topic is a string of topics listed as spaces

        send_message = "{role} {address} {topic}".format(role=self.role, address=self.address, topic=self.topic)
        recv_message = util.lazy_pirate(self.socket, send_message)
        
        self.message = recv_message
        print(self.message)
        if self.message != BABY_PROXY_NO_PUBLISHERS:
            for addr in self.message.split():
                self.publishers.append(addr)

    def notify(self):
        print(self.publishers)

    