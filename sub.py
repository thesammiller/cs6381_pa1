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

from pubsub import subscriber
import weather
import sys

localhost = '127.0.0.1'
use_port = 5556
use_ip = localhost


# API specifies that data will be returned as a string
# first word is the topic
# return Weather data structure
def parse_weather(raw_data):
    zipcode, temperature, humidity = raw_data.split()
    return weather.Weather(zipcode=zipcode, temperature=temperature, humidity=humidity)


# local application processes set number of weather updates
# returns values in dictionary
def average_weather(iterations, weather_update):
    total_temp = 0
    total_humid = 0
    zipcode = None
    print("Getting average of {} weather updates.".format(iterations))

    for i in range(iterations):
        print("Getting update #{}...".format(i+1))

        # function we pass in as argument will return an updated Weather object
        w = weather_update()

        # process the data as needed
        total_temp += w.temperature
        total_humid += w.humidity

        if zipcode is None:
            zipcode = w.zipcode

        if zipcode != w.zipcode:
            print("Error --> inconsistent zip code.")
            break

    # calculate the averages
    avg_temperature = total_temp / iterations
    avg_humidity = total_humid / iterations

    # return data in local data structure
    return weather.Weather(zipcode=zipcode, temperature=avg_temperature, humidity=avg_humidity)


def main():

    if len(sys.argv) > 1:
        print(sys.argv)
        args = sys.argv[::]
        args.pop(0)
        while len(args) > 0:
            if ("-i" in sys.argv):
                use_ip = args.pop(sys.argv.index("-i"))
                args.pop(sys.argv.index("-i") - 1)
                print(use_ip)
                continue
            if ("-p" in sys.argv):
                use_port = args.pop(sys.argv.index("-p"))
                args.pop(sys.argv.index("-p")-1)

    #User Input
    welcome_msg = "Welcome to the Vanderbilt Random Weather Data Service."
    print("*" * len(welcome_msg))
    print(welcome_msg)
    print("*" * len(welcome_msg))

    # determine data of interest
    zipcode = input("What zipcode? > ")

    # create subscriber with interest as topic
    sub = subscriber.NoBrokerSubscriber(port=USE_PORT)

    # variable for local application function
    iterations = int(input("How many iterations? > "))

    # weather logic
    # pass in the update function - lambda so that parameter can be passed to sub notify each time
    # data is returned in a format which can be understood by the local application logic
    avg = average_weather(iterations, lambda: parse_weather(sub.notify(zipcode)))

    print()
    print("*" * len(welcome_msg))

    print("Average temperature " 
            "over {iterations} iterations " 
            "for zipcode {zipcode}:\n" 
            "\tTemperature:\t{temperature:.2f}F\n" 
            "\tHumidity:\t{humidity:.2f}%."
          .format(iterations=iterations, zipcode=zipcode,
                  temperature=avg.temperature, humidity=avg.humidity))

    print("*" * len(welcome_msg))
    print()


if __name__ == '__main__':
    main()

