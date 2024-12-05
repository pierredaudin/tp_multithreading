from manager import QueueClient
from task import Task


def boss():
    # Connexion au gestionnaire de queue
    client = QueueClient()

    # Création et ajout des tâches
    print("Boss: Adding tasks to the queue...")
    for i in range(10):  # Génère 10 tâches
        task = Task(i, 10)
        print(f"Boss: Adding Task {task.identifier} to the queue.")
        client.task_queue.put(task)

    # Signal de fin pour les Minions
    client.task_queue.put(None)
    print("Boss: All tasks added. Waiting for results...\n")

    # Récupération des résultats depuis result_queue
    results = []
    while True:
        result = client.result_queue.get()
        if result is None:
            break  # Signal de fin reçu
        results.append(result)
        print(f"Boss: Received result for Task {result[0]}: {result[1]}")

    print("\nBoss: All results received. Exiting.")
    print("Final Results:")
    for task_id, result in results:
        print(f"Task {task_id}: Result = {result}")

    # Envoyer un signal de fin pour arrêter les Minions
    client.result_queue.put(None)


if __name__ == "__main__":
    boss()
