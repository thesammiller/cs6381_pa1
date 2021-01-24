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
from random import randrange
from pubsub import publisher
import weather


# Format Weather class data
# API requires publishing data as string
def format_data(w):
    return "{temp} {humid}".format(temp=w.temperature, humid=w.humidity)


# local application gets weather data
# then formats data for publishing

if __name__ == '__main__':
    # publisher created with port
    pub = publisher.NoBrokerPublisher(port=5556)
    w = weather.Weather()
    # publish data from local application function that formats data
    # uses a lambda so that get_weather() is called every cycle
    while True:
        w.get_weather()
        # application logic decision to use zipcode as topic
        # Weather stores it as number, retrieve it as string
        topic = str(w.zipcode)
        # format data into publisher string
        data = format_data(w)
        pub.publish(topic, data)

