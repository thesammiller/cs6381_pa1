from messageAPI import FloodSubscriber


fs = FloodSubscriber("90210")
fs.register_sub()
fs.notify()
