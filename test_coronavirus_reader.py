import unittest

from coronavirus_reader import COVID19_Reader

class TestReader(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cvd_reader = COVID19_Reader()
        cls.data = cvd_reader.data_reader()

    def test_dataislist(self):
        self.assertEqual(type(self.data), type([]))

    def test_regex(self):
        date = self.data[-1][0]
        regex = r"(?P<day>\d{2})-(?P<month>\d{2})-(?P<year>\d\d?)"
        self.assertRegex(date, regex)


if __name__ == "__main__":
    unittest.main()
