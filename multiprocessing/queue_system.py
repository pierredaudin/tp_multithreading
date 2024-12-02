from multiprocessing.managers import BaseManager
from multiprocessing import Queue

# Définition des queues partagées
task_queue = Queue()
result_queue = Queue()


# Définition du QueueManager
class QueueManager(BaseManager):
    pass


# Enregistrement des queues
QueueManager.register("get_task_queue", callable=lambda: task_queue)
QueueManager.register("get_result_queue", callable=lambda: result_queue)


# Fonction pour démarrer le QueueManager
def start_queue_manager():
    print("QueueManager: Starting...")
    manager = QueueManager(address=("", 50000), authkey=b"password")
    manager.start()
    print("QueueManager: Running...")
    try:
        while True:  # Maintenir le serveur actif
            pass
    except KeyboardInterrupt:
        print("\nQueueManager: Shutting down...")
    finally:
        manager.shutdown()


# Fonction pour connecter un QueueClient
def connect_to_queue_manager():
    print("QueueClient: Connecting to QueueManager...")
    manager = QueueManager(address=("localhost", 50000), authkey=b"password")
    manager.connect()
    print("QueueClient: Connected.")
    return manager


if __name__ == "__main__":
    start_queue_manager()
