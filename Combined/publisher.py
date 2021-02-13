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



topic = sys.argv[1] if len(sys.argv) > 2 else "90210"


class WeatherPublisher:

    def __init__(self, topic):
        self.topic = topic
        self.pub = Publisher(self.topic)
        self.pub.register_pub()

        
    def generateWeather(self):
        temperature = randrange(-80, 135)
        relhumidity = randrange(10, 60)
        return "{} {}".format(temperature, relhumidity)
        
        
    def weatherPublish(self):
        data = self.generateWeather()
        self.pub.publish("{data}".format(data=data))
        print ("Application sending: {topic} {data}".format(topic=self.topic, data=data))


def main():
    wp = WeatherPublisher(topic)
    while True:
        wp.weatherPublish()
        time.sleep(1)

main()
