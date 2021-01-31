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
#   Weather update server
#   Binds PUB socket to tcp://*:5556
#   Publishes random weather updates
#

import zmq


class NoBrokerPublisher:

    def __init__(self, port=None):
        print("Current libzmq version is %s" % zmq.zmq_version())
        print("Current  pyzmq version is %s" % zmq.__version__)
        
        if port is None:
            self.port = 5556
        else:
            self.port = port

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind("tcp://*:{port}".format(port=self.port))

    def publish(self, topic, data):
        if (type(topic) == str) & (data is not None):
            package = "{topic} {data}".format(topic=topic, data=data)
            self.socket.send_string(package)
