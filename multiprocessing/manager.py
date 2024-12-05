from multiprocessing.managers import BaseManager
from multiprocessing import Queue


# Définition du QueueManager
class QueueClient:
    # Fonction pour connecter un QueueClient
    def __init__(self):
        QueueManager.register("get_task_queue")
        QueueManager.register("get_result_queue")
        print("QueueClient: Connecting to QueueManager...")
        manager = QueueManager(address=("localhost", 50000), authkey=b"password")
        manager.connect()
        print("QueueClient: Connected.")
        self.task_queue = manager.get_task_queue()
        self.result_queue = manager.get_result_queue()


# Définition du QueueManager
class QueueManager(BaseManager):
    pass


if __name__ == "__main__":
    task_queue = Queue()
    result_queue = Queue()
    QueueManager.register("get_task_queue", callable=lambda: task_queue)
    QueueManager.register("get_result_queue", callable=lambda: result_queue)
    m = QueueManager(address=("localhost", 50000), authkey=b"password")
    s = m.get_server()
    s.serve_forever()
