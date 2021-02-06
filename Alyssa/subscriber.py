# Sample code for CS6381

#
#   Weather update client
#   Connects SUB socket to tcp://localhost:5556
#   Collects weather updates and finds avg temp in zipcode
#

import sys


# Determine SubId
srv_addr = sys.argv[1] if len(sys.argv) > 1 else "localhost"
connect_str = "tcp://" + srv_addr + ":5556"

# Determine Sub's interested topic
topic_filter = sys.argv[2] if len(sys.argv) > 2 else "10001"

#register sub to the broker
register_sub(topic_filter, connect_str)


# notify sub of info?????
# notify(topic_filter, what is val )
