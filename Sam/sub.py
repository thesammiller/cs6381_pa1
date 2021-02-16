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

from pubsub import babysubscriber
import weather
import sys




# API specifies that data will be returned as a string
# first word is the topic
# return Weather data structure
def parse_weather(raw_data):
    temperature, humidity = raw_data.split()
    return float(temperature), float(humidity)


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
        w = parse_weather(weather_update())

        # process the data as needed
        total_temp += w[0]
        total_humid += w[1]


    # calculate the averages
    avg_temperature = total_temp / iterations
    avg_humidity = total_humid / iterations

    # return data in local data structure
    return {"temp": avg_temperature, "humidity": avg_humidity}


def main():

    zipcode = '90210' #input("What zipcode? > ")

    sub = babysubscriber.BabySubscriber(zipcode)

    while True:

        iterations = 5 #int(input("How many iterations? > "))

        avg = average_weather(iterations, lambda: sub.listen())


        print("Average temperature " 
          "over {iterations} iterations " 
          "for zipcode {zipcode}:\n" 
          "\tTemperature:\t{temperature:.2f}F\n" 
          "\tHumidity:\t{humidity:.2f}%."
          .format(iterations=iterations, zipcode=zipcode,
                  temperature=avg["temp"], humidity=avg["humidity"]))


if __name__ == '__main__':
    main()
