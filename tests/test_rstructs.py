import sys
sys.path.append("../rstructs/")
from rstructs import rStruct, rList, rSet, rDict, delete_all_temp_objects
import nose
from redis import StrictRedis

def get_redis_connection():
    return StrictRedis(host="127.0.0.1", port=6379, db=9)

def test_rstruct_initialize():
    sr = get_redis_connection()
    r = rStruct(sr)
    assert isinstance(r.list(), rList)
    assert isinstance(r.set(), rSet)
    assert isinstance(r.dict(), rDict)

class Test_rList():
    def setup(self):
        self.sr = sr = get_redis_connection()
        self.r = rStruct(sr)

    def teardown(self):
        delete_all_temp_objects(self.sr)

    def test_instance(self):
        r = self.r
        l = r.list()
        assert isinstance(l, rList)

    def test_length(self):
        r = self.r
        r = r.list([each for each in xrange(0, 10)])
        assert len(r) == 10

    def test_indexoperations(self):
        r = self.r
        l = r.list([1,2,3])
        assert l[0] == '1'
        assert l[1] == '2'
        assert l[2] == '3'

    def test_indexoperations_slice(self):
        r = self.r
        l = r.list([4,5,6])
        del l[1:]
        assert len(l) == 1
        assert l[0] == '4'

    def test_append(self):
        r = self.r
        l = r.list([4,5,6])
        l.append(-1)
        assert len(l) == 4

    def test_extend(self):
        r = self.r
        l_1 = r.list([1,2,3])
        l_2 = r.list([4,5,6])
        l_1.extend(l_2)
        assert isinstance(l_1, rList)
        assert len(l_1) == 6
        temp_list = [each for each in l_1]
        assert temp_list == [str(each) for each in xrange(1,7)]
        # test slicing operations after extend
        temp_list = l_1[:3]
        assert temp_list == [str(each) for each in xrange(1,4)]
        temp_list = l_1[3:]
        assert temp_list == [str(each) for each in xrange(4,7)]

    def test_count(self):
        # list.count to be rewritten
        pass

    def test_index(self):
        return NotImplemented

    def test_pop(self):
        r = self.r
        l = r.list([each for each in xrange(1, 11)])
        val = l.pop()
        assert val == '10'
        assert len(l) == 9
        val = l.pop(0)
        assert val == '1'
        assert len(l) == 8

    def test_remove(self):
        r = self.r
        l = r.list([1,2,3])
        l.remove(1)
        assert len(l) == 2
        temp_list = [i for i in l]
        assert temp_list == [str(each) for each in xrange(2, 4)]

    def test_reverse(self):
        r = self.r
        l = r.list([1,2,3])
        l.reverse()
        temp_list = [i for i in l]
        assert temp_list == [str(each) for each in reversed(range(1, 4))]

class Test_rSet():
    def setup(self):
        self.sr = sr = get_redis_connection()
        self.r = rStruct(sr)

    def teardown(self):
        delete_all_temp_objects(self.sr)

    def test_instance(self):
        r = self.r
        s = r.set()
        assert isinstance(s, rSet)

    def test_instance_init(self):
        r = self.r
        s = r.set([i for i in xrange(0,10)])
        assert len(s) == 10

    def test_length(self):
        r = self.r
        s = r.set([i for i in xrange(0,10)])
        assert len(s) == 10

    def test_and(self):
        r = self.r
        s_1 = r.set([i for i in xrange(0,10)])
        s_2 = r.set([i for i in xrange(-5, 6)])
        s_3 = r.set([i for i in xrange(4, 15)])
        s_empty = r.set([])
        test_set = s_1 & s_2 & s_3
        assert test_set == set(['4', '5'])

    def test_or(self):
        r = self.r
        s_1 = r.set([i for i in xrange(0,10)])
        s_2 = r.set([i for i in xrange(-5, 6)])
        s_3 = r.set([i for i in xrange(4, 15)])
        test_set = s_1 | s_2 | s_3
        assert test_set == set(['11', '1', '13', '12', '7', '14', '0', '6', '10', '-5',
                                '-4', '3', '2', '-1', '4', '-3', '-2', '9', '5', '8'])
    def test_isdisjoint(self):
        r = self.r
        s_1 = r.set([i for i in xrange(0,10)])
        s_2 = r.set([i for i in xrange(-5, 6)])
        s_5 = r.set([i for i in xrange(15, 20)])
        assert s_1.isdisjoint(s_2) == False
        assert s_1.isdisjoint(s_5) == True

    def test_union_store(self):
        r = self.r
        s_4 = r.set([i for i in xrange(4, 8)])
        s_5 = r.set([i for i in xrange(15, 20)])
        s_5 |= s_4
        test_set = s_5
        assert test_set == set(['15', '17', '16', '19', '18', '5', '4', '7', '6'])


class Test_rDict():
    def setup(self):
        self.sr = sr = get_redis_connection()
        self.r = rStruct(sr)

    def teardown(self):
        delete_all_temp_objects(self.sr)

    def test_instance(self):
        r = self.r
        d = r.dict()
        assert isinstance(d, rDict)

    def test_length(self):
        r = self.r
        d = r.dict()
        for each in xrange(0, 10):
            d[each] = each
        assert len(d) == 10

    def test_contains(self):
        r = self.r
        d = r.dict()
        for each in xrange(0, 10):
            d[each] = each
        assert 5 in d

    def test_getitem(self):
        r = self.r
        d = r.dict()
        for each in xrange(0, 10):
            d[each] = each
        assert d[7] == '7'

    def test_keys(self):
        r = self.r
        d = r.dict()
        for each in xrange(0, 10):
            d[each] = each
        assert d.keys() == [str(each) for each in xrange(0, 10)]

    def test_update(self):
        r = self.r
        d = r.dict()
        for each in xrange(0, 10):
            d[each] = each
        temp_d = {each:each for each in xrange(10,20)}
        d.update(temp_d)
        assert len(d) == 20
        assert d.keys() == [str(each) for each in xrange(0, 20)]

    def test___iter__(self):
        r = self.r
        d = r.dict()
        for each in xrange(0, 10):
            d[each] = each
        temp_d = {str(each): str(each) for each in xrange(0, 10)}
        for k in d:
            temp_d.pop(k)
        assert len(temp_d) == 0

    def test_items(self):
        r = self.r
        d = r.dict()
        for each in xrange(0, 10):
            d[each] = each
        temp_d = {str(each): str(each) for each in xrange(0, 10)}
        for k, v in d.items():
            if v == temp_d[k]:
                temp_d.pop(k)
        assert len(temp_d) == 0
