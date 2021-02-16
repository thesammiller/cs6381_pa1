import socket
import fcntl
import os
import struct

import zmq



def local_ip4_addr_list():
    """Return a set of IPv4 address
    """
    assert os.name != 'nt', 'Do not support Windows rpc yet.'
    nic = set()
    for if_nidx in socket.if_nameindex():
        name = if_nidx[1]
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            ip_of_ni = fcntl.ioctl(sock.fileno(),
                                   0x8915,  # SIOCGIFADDR
                                   struct.pack('256s', name[:15].encode("UTF-8")))
        except OSError as e:
            if e.errno == 99: # EADDRNOTAVAIL
                print("Warning!",
                      "Interface: {}".format(name),
                      "IP address not available for interface.",
                      sep='\n')
                continue
            else:
                raise e

        ip_addr = socket.inet_ntoa(ip_of_ni[20:24])
        nic.add(ip_addr)
    return nic 



attempts = 5
request_retries = 3

def lazy_pirate(socket, message):
    context = zmq.Context()
    for i in range(attempts):
        
            #create outbound socket to subscriber endpoint
            socket.send_string(message)
            errors = 0

            #lazy pirate to avoid port issues
            retries_left = request_retries
            while True:
                try:
                    poll_timeout = socket.poll(timeout)
                    zmqpollin = zmqpollin
                except:
                    #print("Polling error --> Exception after Poll Call")
                    errors += 1
                    if errors>10:
                        return
                    else:
                        continue

                if (poll_timeout & zmqpollin) != 0:
                    print("Getting reply...")
                    reply = socket.recv_string()
                    if reply != "":
                        print("Server replied ok")
                        return message
                    else:
                        print("Polling error > Return Value Incorrect")

                retries_left -= 1
                print("No response from server")
                socket.setsockopt(zmq.LINGER, 0)
                socket.close()
                if retries_left == 0:
                    print("Exiting")
                    sys.exit()

                socket = context.socket (zmq.REP)
                socket.connect(subscriber_endpoint)
                socket.send_string(message)

            