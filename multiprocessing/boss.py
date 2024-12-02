from queue_system import connect_to_queue_manager
from task import Task


def boss():
    # Connexion au gestionnaire de queue
    manager = connect_to_queue_manager()
    task_queue = manager.get_task_queue()
    result_queue = manager.get_result_queue()

    # Création et ajout des tâches
    print("Boss: Adding tasks to the queue...")
    for i in range(10):  # Génère 10 tâches
        task = Task(identifier=i)
        print(f"Boss: Adding Task {task.identifier} to the queue.")
        task_queue.put(task)

    # Signal de fin pour les Minions
    task_queue.put(None)
    print("Boss: All tasks added. Waiting for results...\n")

    # Récupération des résultats depuis result_queue
    results = []
    while True:
        result = result_queue.get()
        if result is None:
            break  # Signal de fin reçu
        results.append(result)
        print(f"Boss: Received result for Task {result[0]}: {result[1]}")

    print("\nBoss: All results received. Exiting.")
    print("Final Results:")
    for task_id, result in results:
        print(f"Task {task_id}: Result = {result}")

    # Envoyer un signal de fin pour arrêter les Minions
    result_queue.put(None)


if __name__ == "__main__":
    boss()
