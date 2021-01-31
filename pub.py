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

from pubsub import publisher
import weather

# port for API
USE_PORT = 5556


# helper function to create weather
# returns topic and data strings
def get_weather():
    w = weather.Weather()
    w.get_random_weather()

    # will use zipcode as topic
    # Weather stores zipcode as int
    # API specifies topic as string
    zipcode = str(w.zipcode)

    # weather data temperature and humidity are floats
    # API specifies data as string
    weather_data = format_data(w)

    # return string zipcode as topic
    # return string floats as data
    return zipcode, weather_data


# Format Weather class data
# API requires publishing data as string
def format_data(w):
    return "{temperature} {humidity}".format(temperature=w.temperature, humidity=w.humidity)


# gets weather data
# publishes weather data
if __name__ == '__main__':
    # publisher created with specified port
    pub = publisher.FloodPublisher()

    # publish data from local application function that formats data
    # uses a lambda so that get_weather() is called every cycle
    while True:
        # create topic and data
        topic, data = get_weather()

        # api requires string topic and string data
        pub.publish(topic, data)

