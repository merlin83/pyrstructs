A simple collection of data structures backed by Redis
We try to act as a replacement for python built-in datatypes by mimicing the built in functions

# Motivation

Have you ever written multiple scripts that operated/worked on the same data?

pyrstructs is a way to allow you to use list/sets/dicts as you would in python, but with the ability to share them with other python scripts!
To share the same data, you only have to ensure both objects are of the same type and have the same REDIS_KEY! As easy as that!

# Caveats

All keys and values are stored as strings (This might change in the future)

# Examples

    from redis import StrictRedis
    from rstructs import rStruct
    sr = StrictRedis(host="127.0.0.1", port=6379, db=0)
    r = rStruct(sr)
    # to instantiate a new list/set/dict, if REDIS_KEY is not specified, a random key will be generated which can be accessed with .get_name()
    l = r.list([], REDIS_KEY="FOO_LIST")
    s = r.set([], REDIS_KEY="FOO_SET")
    d = r.dict(REDIS_KEY="FOO_DICT")

# Multiple program example
    # in script one
    l_1 = r.list([1,2,3], REDIS_KEY="FOO_1")
    l_2 = r.list([4,5,6], REDIS_KEY="FOO_2")
    l_1.extend(l_2)
    >> ['1', '2', '3', '4', '5', '6']

    # in script two
    l_1 = r.list(None, REDIS_KEY="FOO_1")
    l_1
    >> ['1', '2', '3', '4', '5', '6']

# List examples (single program)
    l_1 = r.list([1,2,3]) # list is assigned a random keyname
    l_2 = r.list([4,5,6]) # list is assigned a random keyname
    l_1.extend(l_2)
    >> ['1', '2', '3', '4', '5', '6']


# Set examples (single program)
    s_1 = r.set([i for i in xrange(0,10)]) # set is assigned a random keyname
    s_2 = r.set([i for i in xrange(-5, 6)]) # set is assigned a random keyname
    s_3 = r.set([i for i in xrange(4, 15)]) # set is assigned a random keyname
    s_4 = r.set([i for i in xrange(4, 8)]) # set is assigned a random keyname
    s_5 = r.set([i for i in xrange(15, 20)]) # set is assigned a random keyname
    s_empty = r.set([]) # set is assigned a random keyname

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

# Dict examples (single program)
    d = r.dict() # dict is assigned a random keyname
    for each in xrange(0, 10):
        d[each] = each

    temp_d = {each:each for each in xrange(10,20)}
    d.update(temp_d)
    >> {'0': '0', '1': '1', '10': '10', '11': '11', '12': '12', '13': '13',
     '14': '14', '15': '15', '16': '16', '17': '17', '18': '18', '19': '19',
     '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9'}

# To remove all temp objects (keys that were randomly generated)
    from rstructs import delete_all_temp_objects
    delete_all_temp_objects(sr)
