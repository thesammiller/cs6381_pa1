import os
import sys
import time

import zmq
from random import randrange


def get_context():
    context = zmq.Context()
    return context 



def register_pub(topic = <someString>, pubId = connect_str):
    # This is one of many potential publishers, and we are going
    # to send our publications to a proxy. So we use connect
    socket = get_context().socket(zmq.PUB)
    print ("Publisher connecting to proxy at: {}".format(connect_str))
    socket.connect(pubId)

    #what to do with topic here?



def publish(topic = <string>, value = <val>):
    #what to do with topic and val here?
    # keep publishing 
    while True:
        zipcode = randrange(1, 100000)
        temperature = randrange(-80, 135)
        relhumidity = randrange(10, 60)

        #print ("Sending: %i %i %i" % (zipcode, temperature, relhumidity))
        socket.send_multipart("%i %i %i" % (zipcode, temperature, relhumidity))


def register_sub(topic_filter = <someString>, subId):
    # Since we are the subscriber, we use the SUB type of the socket
    socket = get_context().socket(zmq.SUB)

    # Here we assume publisher runs locally unless we
    # send a command line arg like 10.0.0.2
    print("Collecting updates from weather server proxy at: {}".format(subId))
    socket.connect(subId)

    # Python 2 - ascii bytes to unicode str
    if isinstance(topic_filter, bytes):
        topic_filter = topic_filter.decode('ascii')

    # any subscriber must use the SUBSCRIBE to set a subscription, i.e., tell the
    # system what it is interested in
    socket.setsockopt_string(zmq.SUBSCRIBE, topic_filter)
    process_msg() #will print the info






# broker uses to communicate to sub
def notify(topic_filter = <string>, value = <val>)):
    

#how to process and print message in sub
def process_msg():
    # Process 5 updates
    total_temp = 0
    for update_nbr in range(5):
        string = socket.recv_multipart()
        # zipcode, temperature, relhumidity = string.split()
        # total_temp += int(temperature)

        print("Average temperature for zipcode '%s' was %dF" % (
            topic_filter, total_temp / (update_nbr+1))

xsubsocket;
xpubsocket;
poller; 


def create_XSub():
    xsubsocket = get_context.socket(zmq.XSUB)
    xsubsocket.bind("tcp://*:5555")
    return xsubsocket


def create_XPub():
    xpubsocket = get_context.socket (zmq.XPUB)
    xpubsocket.setsockopt(zmq.XPUB_VERBOSE, 1)
    xpubsocket.bind ("tcp://*:5556")
    return xpubsocket

# unsure of parameters
def create_poller(sub = <xsubsocket>, pub = <xpubsocket>):
    poller = zmq.Poller ()
    poller.register (sub, zmq.POLLIN)
    poller.register (pub, zmq.POLLIN)
    return poller

def poll():
    print ("Poll with a timeout of 1 sec")

    events = dict (poller.poll (1000))
    print ("Events received = {}".format (events))

def getPubData():
        # Is there any data from publisher? Note that the proxy
        # will get only that data for which it has relayed
        # subscriptions to the publisher. Note that ZMQ in recent
        # versions is doing filtering on the publisher side. Thus,
        # not all data from publishers will even show up on proxy.
        if xsubsocket in events:
            msg = xsubsocket.recv_multipart()

            print ("Publication = {}".format (msg))

            # send the message to subscribers
            xpubsocket.send_multipart (msg)






def sendSubData():
    # Is there any data from subscriber? Note, this is
        # needed because we must relay the subscription info
        # to all my publishers else they will never send anything
        # to us given that we are a XSUB/XPUB entity
        if xpubsocket in events:
            msg = xpubsocket.recv_multipart()

            # parse the incoming message
            print ("subscription = {}".format (msg))

            # send the subscription info to publishers
            xsubsocket.send_multipart(msg)
