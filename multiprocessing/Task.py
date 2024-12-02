import time


class Task:
    def __init__(self, identifier, size, a, b, x, time_to_work):
        self.identifier = identifier
        self.size = size
        self.a = a
        self.b = b
        self.x = x
        self.time = time_to_work

    def work(self):
        """Simule le travail de la tâche."""
        print(f"Task {self.identifier}: Start working for {self.time} seconds...")
        time.sleep(self.time)  # Simule un délai
        result = self.a * self.x + self.b  # Calcul simple
        print(f"Task {self.identifier}: Finished. Result = {result}")
        return result
