import unittest
import numpy
from task import Task


class TestTask(unittest.TestCase):
    def test_task(self):
        t = Task()
        t.work()
        numpy.testing.assert_allclose(t.a @ t.x, t.b)


if __name__ == "__main__":
    unittest.main()
