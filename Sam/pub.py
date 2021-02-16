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

import sys
import time

from pubsub import babypublisher


if __name__ == '__main__':
    pub = babypublisher.BabyPublisher("90210")
    pub.register_pub()
    while True:
        print("Publishing...")
        data = "32 23"
        pub.publish(data)


