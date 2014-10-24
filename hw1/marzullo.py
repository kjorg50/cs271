# Kyle Jorgensen, CS 271, HW 1, 10/23/14
# This code is built upon https://gist.github.com/tai2/3684493

# c.f. http://en.wikipedia.org/wiki/Marzullo%27s_algorithm
def marzullo_algorithm(ranges):
  table = []
  for l,r in ranges:
    table.append((l,-1))
    table.append((r,+1))

  def my_cmp(x, y):
    result = cmp(x[0], y[0])
    if result == 0:
      result = -cmp(x[1], y[1]) # to exclude 'pathological overlaps'
    return result
  table.sort(my_cmp)

  best = 0
  cnt = 0
  for i in range(len(table) - 1):
    cnt = cnt - table[i][1]
    if best <= cnt:
      best = cnt
      beststart = table[i][0]
      bestend   = table[i+1][0]
  
  # if we had overlapping intervals, return the Marzullo answer
  if best > 1:  
    return (beststart, bestend)
  
  else: # Otherwise, find the two intervals that were closest 
        # and take the midpoints of those two as the result
    cnt = 0
    diff = 9999999 # some large integer
    for i in range(1, len(table)-1, 2):
      cnt = abs(table[i][0] - table[i+1][0])
      if cnt < diff:
        diff = cnt
        mid1 = (table[i-1][0] + table[i][0])/2
        mid2 = (table[i+1][0] + table[i+2][0])/2

    return (mid1, mid2)

    
def test(data_list):
  for data in data_list:
    result = marzullo_algorithm(data['input']) 
    if not result == data['expected']:
      print 'test failed input=', data['input'], 'expected=', data['expected'], 'actual=', result
      return
  print 'test suceeded'

if __name__ == "__main__":
  test_data_list = (
      {'input' : ((8,12),(11,13),(10,12)), 'expected' : (11,12)},
      {'input' : ((8,12),(11,13),(14,15)), 'expected' : (11,12)},
      {'input' : ((8,9),(8,12),(10,12)), 'expected' : (10,12)},
      {'input' : ((8,12),(9,10),(11,13),(10,12)), 'expected' : (11,12)},
      {'input' : ((8,12),(9,10),(11,13),(14,15)), 'expected' : (11,12)},
      {'input' : ((11,15),(8,15),(9,11),(10,14),(11,14),(9,10),(9,13),(12,15),(8,11),(14,15)), 'expected' : (12,13)},
      {'input' : ((-13.0,-11.0),(-6.2,-6.0),(-2.4,-2.2),(4.8,5.0),(6.0,6.4)), 'expected' : (4.9, 6.2)},
      {'input' : ((8.0,9.0),(10.0,11.0),(12.0,13.0)), 'expected' : (8.5,10.5) },
      {'input' : ((1.0,2.0),(2.0,3.0),(4.0,5.0)), 'expected' : (1.5,2.5) })
  test(test_data_list)
 