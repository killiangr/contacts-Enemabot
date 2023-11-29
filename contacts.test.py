import unittest


class MyTestCase(unittest.TestCase):
    def test_should_work_when_doing_stuff(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
