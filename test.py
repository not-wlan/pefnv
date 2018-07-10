import unittest
from pefnv import Export, find_dupes


class TestMatch(unittest.TestCase):
    def setUp(self):
        self.export1 = Export(b'a', "test")
        self.export2 = Export(b'b', "test")
        self.export3 = Export(b'liquid', "test")
        self.export4 = Export(b'costarring', "test")

    def testSame(self):
        assert self.export1.match(self.export1)

    def testDifferent(self):
        assert not self.export1.match(self.export2)

    def testCollision(self):
        assert self.export3.match(self.export4)


class TestCollision(unittest.TestCase):
    def setUp(self):
        self.exports = [
            Export(b'liquid', "test"),
            Export(b'costarring', "test")
        ]

    def testFindCollision(self):
        assert len(find_dupes(self.exports)) == 2


class TestDupe(unittest.TestCase):
    def setUp(self):
        self.exports = [
            Export(b'test', "test"),
            Export(b'test', "test")
        ]

    def testFindDupe(self):
        assert len(find_dupes(self.exports)) == 0


class TestDifferent(unittest.TestCase):
    def setUp(self):
        self.exports = [
            Export(b'a', "test"),
            Export(b'b', "test")
        ]

    def testFindNone(self):
        assert len(find_dupes(self.exports)) == 0

