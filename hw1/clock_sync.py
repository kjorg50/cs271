#!/usr/bin/python
# Kyle Jorgensen, CS 271, HW 1, 10/20/14

import socket
import sys
from datetime import datetime, timedelta

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
      s.sendto(msg.encode('utf-8'), (host5, port2))

      t_local = datetime.now()

      # receive data from time server (data, addr)
      d = s.recvfrom(1024) # buffer size 1024 bytes
      t_recv = datetime.now()

      # Round trip time (timedelta obj)
      t_round = t_recv - t_send
      rtt = t_round.total_seconds()

      # The time received from the server
      reply = d[0].decode("utf-8")
      reply_float = float(reply)
      t_server = datetime.fromtimestamp(reply_float)

      # time reported from the server plus RTT/2
      t_server_corrected = t_server + timedelta(seconds=(rtt/2))

      print ('Server reply: ' + str(t_server) )
      print("RTT: " + str(rtt) )
      print("**local time: " + str(t_recv) )
      #print("**reply float: " + str( t_server ) )
      print("Diff: " + str( (t_local - t_server_corrected).total_seconds() ) + '\n')
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