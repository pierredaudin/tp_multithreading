import time
import json
import numpy as np


class Task:
    def __init__(self, identifier=0, size=None):
        self.identifier = identifier
        # choosee the size of the problem
        self.size = size or np.random.randint(300, 3_000)
        # Generate the input of the problem
        self.a = np.random.rand(self.size, self.size)
        self.b = np.random.rand(self.size)
        # prepare room for the results
        self.x = np.zeros((self.size))
        self.time = 0

    def work(self):
        start = time.perf_counter()
        self.x = np.linalg.solve(self.a, self.b)
        self.time = time.perf_counter() - start

    def to_json(self):
        task_dict = {
            "identifier": self.identifier,
            "size": self.size,
            "a": np.tolist(self.a),  # converison de matrice à liste
            "b": np.tolist(self.b),
            "x": np.tolist(self.x),
            "time": self.time,
        }
        return json.dumps(task_dict)

    @staticmethod
    def from_json(text: str):
        task_dict = json.loads(text)
        task = Task()
        task.identifier = task_dict["identifier"]
        task.size = task_dict["size"]
        task.a = np.array(task_dict["a"])
        task.b = np.array(task_dict["b"])
        task.x = np.array(task_dict["x"])
        task.time = task_dict["time"]
        return task

    def __eq__(self, other: "Task"):
        if not isinstance(other, Task):
            return False
        return (
            self.identifier == other.identifier
            and self.size == other.size
            and np.array_equal(self.a, other.a)
            and np.array_equal(self.b, other.b)
            and np.array_equal(self.x, other.x)
            and self.time == other.time
        )
