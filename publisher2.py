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
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#
# Added more comments

import sys

import zmq
import time

REQUEST_TIMEOUT = 5000
REQUEST_RETRIES = 3
SERVER_ENDPOINT = "tcp://localhost:5555"

context = zmq.Context()

print ("Publisher...")
socket = context.socket(zmq.REQ)

# Here we assume a server runs locally unless we
# send a command line arg like 10.0.0.2
srv_addr = sys.argv[1] if len(sys.argv) > 1 else "localhost"
connect_str = "tcp://" + srv_addr + ":5555"
socket.connect(connect_str)

for i in range(10):
    print("Sending " + str(i))
    message = "Message" + str(i)
    socket.send_string(message)
    
    #lazy pirate to avoid port issues
    retries_left = REQUEST_RETRIES
    while True:
        #print("Socket poll and zmq pollin")
        if (socket.poll(REQUEST_TIMEOUT) & zmq.POLLIN) != 0:
            print("Getting reply...")
            reply = socket.recv_string()
            if reply == message:
                print("Server replied ok")
                break
            else:
                print("Polling error")
                continue

        retries_left -= 1
        print("No response from server")
        socket.setsockopt(zmq.LINGER, 0)
        socket.close()
        if retries_left == 0:
            print("Exiting")
            sys.exit()

        socket = context.socket(zmq.REQ)
        socket.connect(SERVER_ENDPOINT)
        socket.send_string(message)
