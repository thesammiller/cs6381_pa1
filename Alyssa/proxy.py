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

# system and time
import os
import sys
import time

import zmq
from random import randrange
from messageAPI import Proxy

print ("ZMQ version = {}, PyZMQ version = {}".format (zmq.zmq_version (), zmq.pyzmq_version ()))
       
# Get the context   
# context = zmq.Context()

# This is a proxy. We create the XSUB and XPUB endpoints
xsub = create_XSub()
xpub = create_XPub()

# Now we are going to create a poller
poller = create_poller(xsub, xpub)

while True:
    try:
        
        poll()
        getPubData()
        sendSubData()
        
    except:
        print("Exception thrown: ", sys.exc_info()[0])

