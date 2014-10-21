#!/usr/bin/python
# Kyle Jorgensen, CS 271, HW 1, 10/20/14

import socket
import sys
import time

try:
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
  print ('Failed to create socket')
  sys.exit()

host1 = '54.169.67.45'
host2 = '54.207.15.207'
host3 = '54.191.73.92'
port = 5000

while(True):
  try:
    msg = 'time' # this message doesn't matter, it just needs to be non-empty

    # Semd the request to the server
    t_send = time.clock_gettime(time.CLOCK_REALTIME)
    s.sendto(msg.encode('utf-8'), (host1, port))

    t_local = time.clock_gettime(time.CLOCK_REALTIME)

    # receive data from time server 1 (data, addr)
    d = s.recvfrom(1024) # buffer size 1024 bytes
    t_recv = time.clock_gettime(time.CLOCK_REALTIME)
    t_round = t_recv - t_send

    reply = d[0].decode("utf-8")
    reply_float = float(reply)

    #print ('Server reply: ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(reply_float)) )
    print("RTT: " + str(t_round))
    print("Diff: " + str( t_local - (reply_float + t_round/2)) + '\n')
    #print("current time: " + str(time.clock_gettime(time.CLOCK_REALTIME)) + " server w/ adj: " 
     #     + str(reply_float + t_round/2))

  # some problem seding data?
  except socket.error as e:
    print ('Error Code: ' + str(e[0]) + ' Message ' + e[1])
    sys.exit()

  # ctrl-C
  except KeyboardInterrupt:
    break

print('Program Complete')