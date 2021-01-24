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
#   Weather update client
#   Connects SUB socket to tcp://localhost:5556
#   Collects weather updates and finds avg temp in zipcode
#

import zmq


class NoBrokerSubscriber:

    def __init__(self, srv_addr="localhost", port=5556, topic="10001"):
        #  Socket to talk to server
        self.context = zmq.Context()

        # Since we are the subscriber, we use the SUB type of the socket
        self.socket = self.context.socket(zmq.SUB)

        # Here we assume publisher runs locally unless we
        # send a command line arg like 10.0.0.1
        self.srv_addr = srv_addr
        self.port = port

        self.connect_str = "tcp://{addr}:{port}".format(addr=self.srv_addr, port=self.port)

    def notify(self, topic):
        self.socket.connect(self.connect_str)
        # Python 2 - ascii bytes to unicode str
        if isinstance(topic, bytes):
            topic = topic.decode('ascii')
        # any subscriber must use the SUBSCRIBE to set a subscription, i.e., tell the
        # system what it is interested in
        self.socket.setsockopt_string(zmq.SUBSCRIBE, topic)

        return self.socket.recv_string()
