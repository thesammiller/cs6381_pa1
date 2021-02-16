from pubsub import babybroker

def main():
    print("Creating babybroker.")
    b = babybroker.BabyBroker()
    print("Running babybroker.")
    b.run()
    print("This comes after a true loop and should not be visible.")
    print("Error in the application for Baby Broker.")

if __name__ == '__main__':
    main()
