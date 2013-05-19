A simple collection of data structures backed by Redis
We try to act as a replacement for python built-in datatypes by mimicing the built in functions

Examples

from redis import StrictRedis
from rstructs import rStruct
sr = StrictRedis(host="127.0.0.1", port=6379, db=0)
r = rStruct(sr)

# List examples
l_1 = r.list([1,2,3])
l_2 = r.list([4,5,6])
l_1.extend(l_2)
>> ['1', '2', '3', '4', '5', '6']

# Set examples
s_1 = r.set([i for i in xrange(0,10)])
s_2 = r.set([i for i in xrange(-5, 6)])
s_3 = r.set([i for i in xrange(4, 15)])
s_4 = r.set([i for i in xrange(4, 8)])
s_5 = r.set([i for i in xrange(15, 20)])
s_empty = r.set([])

s_1 & s_2 & s_3
>> set(['5', '4'])
s_1 | s_2 | s_3
>> set(['11', '1', '13', '12', '7', '14', '0', '6', '10', '-5',
       '-4', '3', '2', '-1', '4', '-3', '-2', '9', '5', '8'])
s_1.isdisjoint(s_2)
>> False
s_1.isdisjoint(s_5)
>> True
s_5 |= s_4
print s_5
>> set(['15', '17', '16', '19', '18', '5', '4', '7', '6'])

# Dict examples
d = r.dict()
for each in xrange(0, 10):
    d[each] = each

temp_d = {each:each for each in xrange(10,20)}
d.update(temp_d)

# To remove them all
from structs import delete_all_temp_objects
delete_all_temp_objects(sr)
