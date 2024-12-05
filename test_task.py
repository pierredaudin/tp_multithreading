import unittest
import numpy
from task import Task


class TestTask(unittest.TestCase):
    def test_task(self):
        t = Task()
        t.work()
        numpy.testing.assert_allclose(t.a @ t.x, t.b)

    def test_serail_deserial():
        a = Task()
        txt = a.to_json()
        b = Task.from_json(txt)
        numpy.testing.assert_equal(a, b)


if __name__ == "__main__":
    unittest.main()
