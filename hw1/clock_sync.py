#!/usr/bin/python
# Kyle Jorgensen, CS 271, HW 1, 10/20/14

import socket
import sys
from datetime import datetime, timedelta
import marzullo

host1 = '54.169.67.45'
host2 = '54.207.15.207'
host3 = '54.191.73.92'
host4 = '54.172.168.244'
host5 = '128.111.44.106'
port = 5000
port2 = 12291 # only to be used with host5

def sync():
  '''
    Performs the clock synchronization using my altered Marzullo's algorithm
  '''
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  except socket.error:
    print ('Failed to create socket')
    sys.exit()

  while(True):
    try:
      msg = 'time' # this message doesn't matter, it just needs to be non-empty

      # Send the request to the server
      t_send_1 = datetime.now()
      s.sendto(msg.encode('utf-8'), (host1, port))

      # receive data from time server (data, addr)
      data_1 = s.recvfrom(1024) # buffer size 1024 bytes
      t_recv_1 = datetime.now()

      # Round trip time (timedelta obj)
      t_round_1 = t_recv_1 - t_send_1
      rtt_1 = t_round_1.total_seconds()

      # The time received from the server
      reply_float_1 = float(data_1[0].decode("utf-8"))
      t_server_1 = datetime.fromtimestamp(reply_float_1)

      # time reported from the server plus RTT/2
      t_server_1_corrected = t_server_1 + timedelta(seconds=(rtt_1/2))

      # Get times from servers 2 - 5
      t_send_2 = datetime.now()
      s.sendto(msg.encode('utf-8'), (host2, port))
      data_2 = s.recvfrom(1024) 
      t_recv_2 = datetime.now()
      t_round_2 = t_recv_2 - t_send_2
      rtt_2 = t_round_2.total_seconds()
      reply_float_2 = float(data_2[0].decode("utf-8"))
      t_server_2 = datetime.fromtimestamp(reply_float_2)
      t_server_2_corrected = t_server_2 + timedelta(seconds=(rtt_2/2))

      t_send_3 = datetime.now()
      s.sendto(msg.encode('utf-8'), (host3, port))
      data_3 = s.recvfrom(1024) 
      t_recv_3 = datetime.now()
      t_round_3 = t_recv_3 - t_send_3
      rtt_3 = t_round_3.total_seconds()
      reply_float_3 = float(data_3[0].decode("utf-8"))
      t_server_3 = datetime.fromtimestamp(reply_float_3)
      t_server_3_corrected = t_server_3 + timedelta(seconds=(rtt_3/2))

      t_send_4 = datetime.now()
      s.sendto(msg.encode('utf-8'), (host4, port))
      data_4 = s.recvfrom(1024) 
      t_recv_4 = datetime.now()
      t_round_4 = t_recv_4 - t_send_4
      rtt_4 = t_round_4.total_seconds()
      reply_float_4 = float(data_4[0].decode("utf-8"))
      t_server_4 = datetime.fromtimestamp(reply_float_4)
      t_server_4_corrected = t_server_4 + timedelta(seconds=(rtt_4/2))

      t_send_5 = datetime.now()
      s.sendto(msg.encode('utf-8'), (host5, port2))
      data_5 = s.recvfrom(1024) 
      t_recv_5 = datetime.now()
      t_round_5 = t_recv_5 - t_send_5
      rtt_5 = t_round_5.total_seconds()
      reply_float_5 = float(data_5[0].decode("utf-8"))
      t_server_5 = datetime.fromtimestamp(reply_float_5)
      t_server_5_corrected = t_server_5 + timedelta(seconds=(rtt_5/2))

      ######## Clock Shifting ########

      # shift each server time backward to make it as if they 
      # all responded at the same time
      t_server_2 = t_server_2 - (t_send_2 - t_send_1)
      t_server_3 = t_server_3 - (t_send_3 - t_send_1)
      t_server_4 = t_server_4 - (t_send_4 - t_send_1)
      t_server_5 = t_server_5 - (t_send_5 - t_send_1)

      ##### Marzullo Calculation #####
      update_range = calc_marzullo(t_server_1,t_server_2,t_server_3,t_server_4,t_server_5,
                                   t_round_1,t_round_2,t_round_3,t_round_4,t_round_5)
      update_middle = (update_range[0] + update_range[1])/2
      t_update = datetime.fromtimestamp(update_middle) 

      ############ Outputs ###########

      print("Current (local) time: " + str(t_send_1) )
      print('Server 1 time       : ' + str(t_server_1) + " | RTT to server1 (sec): " + str(rtt_1))
      # print("RTT to server1 (sec): " + str(rtt_1) )

      print('Server 2 time       : ' + str(t_server_2) + " | RTT to server2 (sec): " + str(rtt_2))
      # print("RTT to server2 (sec): " + str(rtt_2) )

      print('Server 3 time       : ' + str(t_server_3) + " | RTT to server3 (sec): " + str(rtt_3))
      # print("RTT to server3 (sec): " + str(rtt_3) )

      print('Server 4 time       : ' + str(t_server_4) + " | RTT to server4 (sec): " + str(rtt_4))
      # print("RTT to server4 (sec): " + str(rtt_4) )

      print('Server 5 time       : ' + str(t_server_5) + " | RTT to server5 (sec): " + str(rtt_5))
      # print("RTT to server5 (sec): " + str(rtt_5) )

      print("Updated time        : " + str(t_update) + '\n')
      print("******************************\n")

    # some problem seding data?
    except socket.error as e:
      print ('Error Code: ' + str(e[0]) + ' Message ' + e[1])
      sys.exit()

    # ctrl-C
    except KeyboardInterrupt:
      break

def calc_marzullo(ts1, ts2, ts3, ts4, ts5, 
                  rtt1, rtt2, rtt3, rtt4, rtt5):
  '''
    Takes in all of the server times and round trip times, 
    then inputs them into the Marzullo algorithm to get a 
    result. The final range is returned as a tuple
  '''
  test_list = ((unix_time(ts1-rtt1),unix_time(ts1+rtt1)),
               (unix_time(ts2-rtt2),unix_time(ts2+rtt2)),
               (unix_time(ts3-rtt3),unix_time(ts3+rtt3)),
               (unix_time(ts4-rtt4),unix_time(ts4+rtt4)),
               (unix_time(ts5-rtt5),unix_time(ts5+rtt5)))

  result = marzullo.marzullo_algorithm(test_list)
  return result

def unix_time(dt):
    epoch = datetime.utcfromtimestamp(0)
    # need the timedelta to offset the values back to normal
    delta = (dt - epoch) + timedelta(hours=7)
    return delta.total_seconds()


if __name__ == "__main__":
  sync()  

  print('Program Complete')