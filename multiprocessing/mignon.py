from manager import QueueClient


def minion():
    # Connexion au gestionnaire de queue
    client = QueueClient()
    task_queue = client.task_queue  # Utiliser directement la file de tâches
    result_queue = client.result_queue  # Utiliser directement la file de résultats

    print("Minion: Prêt à faire les tâches")
    while True:
        # Récupérer une tâche depuis la file
        task = task_queue.get()
        if task is None:  # Vérifier si un signal de fin a été envoyé
            print("Minion: Plus de tâches à faire")
            task_queue.put(None)  # Répercuter le signal pour les autres Minions
            break
        print(f"Minion: Tâche {task.identifier} en cours")

        # Effectuer la tâche
        task.work()

        # Envoyer le résultat dans la file de résultats
        result_queue.put(task)
    print("Minion: Tâches terminées")


if __name__ == "__main__":
    minion()
