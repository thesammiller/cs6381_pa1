from messageAPI import FloodSubscriber


fs = FloodSubscriber()
fs.register_sub("90210")
fs.notify()
