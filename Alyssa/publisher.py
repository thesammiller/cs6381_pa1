# Sample code for CS6381
# Vanderbilt University
# Instructor: Aniruddha Gokhale
#
# Code based on basic pub/sub but modified for xsub and xpub
#
# We are executing these samples on a Mininet-emulated environment
#
#

#
#   Weather update server
#   Publishes random weather updates
#  Connects to a xsub on port 5555
#

import sys
import time
import zmq
from random import randrange
from messageAPI import Proxy, Publisher


pub = Publisher()

srv_addr = sys.argv[1] if len(sys.argv) > 1 else "localhost"
proxy_address = "tcp://" + srv_addr + ":5555"

pub.register_pub("90210", proxy_address)
# This is one of many potential publishers, and we are going
# to send our publications to a proxy. So we use connect
#socket = context.socket(zmq.PUB)
print ("Publisher connecting to proxy at: {}".format(proxy_address))
#socket.connect(connect_str)

# keep publishing 
while True:
    zipcode = 90210 #randrange(1, 100000)
    temperature = randrange(-80, 135)
    relhumidity = randrange(10, 60)

    print ("Sending: %i %i %i" % (zipcode, temperature, relhumidity))
    pub.publish(str(zipcode), "{} {}".format(temperature, relhumidity))
    time.sleep(1)
