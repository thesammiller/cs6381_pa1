# Sample code for CS6381

#
#   Weather update client
#   Connects SUB socket to tcp://localhost:5556
#   Collects weather updates and finds avg temp in zipcode
#

import sys
from messageAPI import Subscriber


topic_filter = sys.argv[1] if len(sys.argv) > 2 else "90210"

class WeatherSubscriber:

    def __init__(self, topic):
        self.sub = Subscriber(topic)
        self.topic = topic
        self.sub.register_sub()


    def run(self):
        total_temp = 0
        for update_nbr in range(5):
            string = self.sub.process_msg()
            zipcode, temperature, relhumidity = string.split(" ")
            total_temp += int(temperature)

        print("Average temperature for zipcode '%s' was %dF" % (zipcode, total_temp / (update_nbr+1)))

def main():
    ws = WeatherSubscriber(topic_filter)
    while True:
        ws.run()

main()



