# weather 'library'
# provides a common data structure for applications

from random import randrange


class Weather:
    def __init__(self, zipcode=int(), temperature=float(), humidity=float()):
        self.set_zipcode(zipcode)
        self.set_temperature(temperature)
        self.set_humidity(humidity)

    def get_weather(self):
        # produce weather data
        self.set_zipcode(randrange(1, 100000))
        self.set_temperature(randrange(-80, 135))
        self.set_humidity(randrange(10, 60))
        return self

    def set_temperature(self, temp):
        try:
            self.temperature = float(temp)
        except ValueError:
            print("invalid temperature")

    def set_humidity(self, humid):
        try:
            self.humidity = float(humid)
        except ValueError:
            print("invalid humidity")

    def set_zipcode(self, zipcode):
        try:
            self.zipcode = int(zipcode)
        except ValueError:
            print("invalid zipcode")




