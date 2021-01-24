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

#data structure for weather information
#dictionary with keys 'zip', 'temp', 'humid'

from pubsub import subscriber
import weather


# API specifies that data will be returned as a string
# first word is the topic
def parse_weather(raw_data):
    zipcode, temp, humid = raw_data.split()
    w = weather.Weather()
    w.set_zipcode(zipcode)
    w.set_temperature(temp)
    w.set_humidity(humid)
    return w


# local application processes set number of weather updates
# returns values in weather data structure
def average_weather(iterations, weather_update):
    total_temp = 0
    total_humid = 0
    zipcode = None
    print("Getting average of {} weather updates.".format(iterations))

    for i in range(iterations):
        print("Getting update #{}...".format(i+1))
        # get data in local format
        raw_data = weather_update()
        w = parse_weather(raw_data)

        # process the data as needed
        total_temp += w.temperature
        total_humid += w.humidity

        if zipcode is None:
            zipcode = w.zipcode

        if zipcode != w.zipcode:
            print("Error --> inconsistent zip code.")
            break

    # calculate the averages
    temp = total_temp / iterations
    humid = total_humid / iterations

    # return data in familiar data structure
    return {"zip": zipcode, "temp": temp, "humid": humid}


def main():
    welcome_msg = "Welcome to the Vanderbilt Random Weather Data Service."
    print("*" * len(welcome_msg))
    print(welcome_msg)
    print("*" * len(welcome_msg))
    # determine data of interest
    zipcode = input("What zipcode? > ")

    # create subscriber with interest as topic
    sub = subscriber.NoBrokerSubscriber(topic=zipcode)

    # variable for local application function
    iterations = int(input("How many iterations? > "))

    # local function gets passed main arguments
    # pass in the update function
    # data is returned in a format which can be understood by the local application logic
    data = average_weather(iterations, lambda: sub.notify(zipcode))


    print()
    print("*" * len(welcome_msg))
    print("Average temperature " 
                "over {iterations} iterations " 
                "for zipcode {zip}:\n" 
                "\tTemperature:\t{temp:.2f}F\n" 
                "\tHumidity:\t{humid:.2f}%."
          .format(iterations=iterations, **data))
    print("*" * len(welcome_msg))

if __name__ == '__main__':
    main()

