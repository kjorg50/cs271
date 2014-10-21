#!/usr/bin/python
# Kyle Jorgensen, CS 271, HW 1, 10/20/14

import socket
import sys  

try:
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
  print ('Failed to create socket')
  sys.exit()

host1 = '54.169.67.45'
port = 5000

while(True):
  try:
    msg = 'time' # this message doesn't matter, it just needs to be non-empty

    #print("Getting time...")
    # Set the whole string
    s.sendto(msg.encode('utf-8'), (host1, port))

    # receive data from time server 1 (data, addr)
    d = s.recvfrom(1024) # buffer size 1024 bytes
    reply = d[0]
    addr = d[1]
    
    print ('Server reply : ' + reply.decode("utf-8"))

  # some problem seding data?
  except socket.error as e:
    print ('Error Code : ' + str(e[0]) + ' Message ' + e[1])
    sys.exit()

  # ctrl-C
  except KeyboardInterrupt:
    break

print('Program Complete')