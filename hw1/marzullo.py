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
        if best < cnt:
            best = cnt
            beststart = table[i][0]
            bestend   = table[i+1][0]
    return (beststart, bestend)
        
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
            {'input' : ((8,9),(8,12),(10,12)), 'expected' : (8,9)},
            {'input' : ((8,12),(9,10),(11,13),(10,12)), 'expected' : (11,12)},
            {'input' : ((8,12),(9,10),(11,13),(14,15)), 'expected' : (9,10)},
            {'input' : ((11,15),(8,15),(9,11),(10,14),(11,14),(9,10),(9,13),(12,15),(8,11),(14,15)), 'expected' : (12,13)})
    test(test_data_list)