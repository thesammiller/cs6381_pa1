# Sample code for CS6381

#
#   Weather update client
#   Connects SUB socket to tcp://localhost:5556
#   Collects weather updates and finds avg temp in zipcode
#

import sys
from messageAPI import Subscriber

srv_addr = sys.argv[1] if len(sys.argv) > 1 else "localhost"
topic_filter = sys.argv[2] if len(sys.argv) > 2 else "90210"

class WeatherSubscriber:

    def __init__(self, topic, srv_addry):
        self.sub = Subscriber(topic)
        self.connect_str = "tcp://" + srv_addr + ":5556"
        self.topic = topic
        self.sub.register_sub(self.connect_str)


    def run(self):
        total_temp = 0
        for update_nbr in range(5):
            string = self.sub.process_msg()
            zipcode, temperature, relhumidity = string.split(" ")
            total_temp += int(temperature)

        print("Average temperature for zipcode '%s' was %dF" % (zipcode, total_temp / (update_nbr+1)))

def main():
    ws = WeatherSubscriber(topic_filter, srv_addr)
    while True:
        ws.run()

main()



