from manager import QueueClient


def minion():
    # Connexion au gestionnaire de queue
    client = QueueClient()
    task_queue = client.get_task_queue()
    result_queue = client.get_result_queue()

    print("Minion: Prêt à faire les tâches")
    while True:
        task = task_queue.get()
        if task is None:
            print("Minion: Plus de tâches à faire")
            task_queue.put(None)
            break
        print(f"Minion: Tâche {task.identifier} en cours")
        result = task.work()
        result_queue.put((task.identifier, result))
    print("Minion: Tâches terminées")


if __name__ == "__main__":
    minion()
