import os
import sys
import time

import zmq
from random import randrange
from collections import defaultdict


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

    def __init__(self):
        self.context = zmq.Context()
        self.socket = None

    def register_pub(self, topic, pubId):
        self.socket = self.context.socket(zmq.PUB)
        print("Publisher connecting to proxy at: {}".format(pubId))
        self.socket.connect(pubId)
        

    def publish(self, topic, value):
        #what to do with topic and val here?
        #I think that the topic for the below is zipcode
        # the value is temperature and humidity
        # so this should just take topic and value and then send them
        #to the broker
        # I think the while True loop would be in the App logic
        # something might publish constantly, but something else 
        # might only publish once or twice

        # keep publishing 
        '''
        while True:
            zipcode = randrange(1, 100000)
            temperature = randrange(-80, 135)
            relhumidity = randrange(10, 60)
        '''
        print ("Message API Sending: {} {}".format(topic, value))
        self.socket.send_string("{topic} {value}".format(topic=topic, value=value))


class Subscriber:

    def __init__(self):
        self.context = zmq.Context()

    def register_sub(self, topic_filter, subId):
        # Since we are the subscriber, we use the SUB type of the socket
        self.socket = self.context.socket(zmq.SUB)

        # Here we assume publisher runs locally unless we
        # send a command line arg like 10.0.0.2
        print("Collecting updates from weather server proxy at: {}".format(subId))
        self.socket.connect(subId)

        # Python 2 - ascii bytes to unicode str
        # We won't be using Python2 - default is Python3 on Ubuntu 20.20
        '''
        if isinstance(topic_filter, bytes):
            topic_filter = topic_filter.decode('ascii')
        '''
        
        # any subscriber must use the SUBSCRIBE to set a subscription, i.e., tell the
        # system what it is interested in
    
        self.socket.setsockopt_string(zmq.SUBSCRIBE, topic_filter)




    #how to process and print message in sub
    def process_msg(self):
                                   # Process 5 updates
        total_temp = 0
        for update_nbr in range(5):
                string = self.socket.recv_string()
                zipcode, temperature, relhumidity = string.split(" ")
                total_temp += int(temperature)

        print("Average temperature for zipcode '%s' was %dF" % (zipcode, total_temp / (update_nbr+1)))
