#!/usr/bin/python
# Kyle Jorgensen, CS 271, HW 1, 10/20/14

import socket
import sys
from datetime import datetime

host1 = '54.169.67.45'
host2 = '54.207.15.207'
host3 = '54.191.73.92'
host4 = '54.172.168.244'
host5 = '128.111.44.106'
port = 5000
port2 = 12291 # only to be used with host5

def sync():
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  except socket.error:
    print ('Failed to create socket')
    sys.exit()

  while(True):
    try:
      msg = 'time' # this message doesn't matter, it just needs to be non-empty

      # Send the request to the server
      t_send = datetime.now()
      s.sendto(msg.encode('utf-8'), (host1, port))

      # receive data from time server (data, addr)
      d = s.recvfrom(1024) # buffer size 1024 bytes
      #t_local = datetime.now()
      t_recv = datetime.now()

      # Round trip time (timedelta obj)
      t_round = t_recv - t_send
      rtt = t_round.total_seconds()

      # The time received from the server
      reply = d[0].decode("utf-8")
      reply_float = float(reply)

      print ('Server reply: ' + datetime.fromtimestamp(reply_float).strftime('%Y-%m-%d %H:%M:%S.%f') )
      print("RTT: " + str(rtt) )
      # print("**recv time: " + str(t_recv.timestamp()) )
      # print("**reply float: " + str(reply_float) )
      print("Diff: " + str( t_recv.timestamp() - (reply_float + rtt/2)) + '\n')
      #print("current time: " + str(time.clock_gettime(time.CLOCK_REALTIME)) + " server w/ adj: " 
       #     + str(reply_float + t_round/2))

    # some problem seding data?
    except socket.error as e:
      print ('Error Code: ' + str(e[0]) + ' Message ' + e[1])
      sys.exit()

    # ctrl-C
    except KeyboardInterrupt:
      break

if __name__ == "__main__":
  sync()
  print('Program Complete')