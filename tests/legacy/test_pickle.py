import pickle
from io import BytesIO
from unittest import TestCase


class TestPickle(TestCase):
    def do_pickle_test(self, ipt):
        buffer = BytesIO()
        pickle.dump(ipt, buffer, pickle.HIGHEST_PROTOCOL)
        buffer.seek(0)
        opt = pickle.load(buffer)
        return ipt is opt

    def test_pickle(self):
        from tests.pickle_enums import Color, PriorityEx

        self.assertTrue(self.do_pickle_test(PriorityEx.ONE))
        self.assertTrue(self.do_pickle_test(PriorityEx.TWO))
        self.assertTrue(self.do_pickle_test(PriorityEx.THREE))

        self.assertTrue(self.do_pickle_test(PriorityEx("1")))
        self.assertTrue(self.do_pickle_test(PriorityEx("2")))
        self.assertTrue(self.do_pickle_test(PriorityEx(3)))

        self.assertTrue(self.do_pickle_test(Color.RED))
        self.assertTrue(self.do_pickle_test(Color.GREEN))
        self.assertTrue(self.do_pickle_test(Color.BLUE))

    def test_flag_pickle(self):
        from tests.pickle_enums import IntPerm, Perm

        self.assertTrue(self.do_pickle_test(Perm.R))
        self.assertTrue(self.do_pickle_test(Perm.W))
        self.assertTrue(self.do_pickle_test(Perm.X))
        self.assertTrue(self.do_pickle_test(Perm.RWX))
        self.assertTrue(self.do_pickle_test(Perm.R | Perm.W | Perm.X))
        self.assertTrue(self.do_pickle_test(Perm.R | Perm.W))

        self.assertTrue(self.do_pickle_test(IntPerm.R))
        self.assertTrue(self.do_pickle_test(IntPerm.W))
        self.assertTrue(self.do_pickle_test(IntPerm.X))
        self.assertTrue(self.do_pickle_test(IntPerm.RWX))
        self.assertTrue(self.do_pickle_test(IntPerm.R | IntPerm.W | IntPerm.X))
        self.assertTrue(self.do_pickle_test(IntPerm.W | IntPerm.X))
