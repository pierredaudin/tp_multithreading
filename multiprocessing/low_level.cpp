#include <Eigen/Dense>
#include <cpr/cpr.h>
#include <iostream>
#include <nlohmann/json.hpp>

// Namespace pour JSON
using json = nlohmann::json;

// Classe représentant une tâche
class Task {
public:
  int identifier;
  int size;
  Eigen::MatrixXd a;
  Eigen::VectorXd b;
  Eigen::VectorXd x;
  double time;

  // Constructeur vide
  Task() : identifier(0), size(0), time(0) {}

  // Constructeur à partir d'un JSON
  explicit Task(const json &task_json) {
    identifier = task_json.at("identifier").get<int>();
    size = task_json.at("size").get<int>();
    a = Eigen::MatrixXd(size, size);
    b = Eigen::VectorXd(size);

    // Charger les données de la matrice et du vecteur
    for (int i = 0; i < size; ++i) {
      b[i] = task_json.at("b")[i];
      for (int j = 0; j < size; ++j) {
        a(i, j) = task_json.at("a")[i][j];
      }
    }

    x = Eigen::VectorXd::Zero(size);
    time = 0;
  }

  // Méthode pour effectuer le travail
  json work() {
    auto start = std::chrono::high_resolution_clock::now();
    x = a.colPivHouseholderQr().solve(b); // Résolution de l'équation Ax = b
    auto end = std::chrono::high_resolution_clock::now();

    time = std::chrono::duration<double>(end - start).count();

    // Préparer le résultat en format JSON
    json result_json;
    result_json["identifier"] = identifier;
    result_json["time"] = time;
    result_json["x"] = std::vector<double>(x.data(), x.data() + x.size());
    return result_json;
  }
};

int main() {
  std::cout << "Minion: Prêt à récupérer les tâches depuis le proxy"
            << std::endl;

  while (true) {
    // Récupérer une tâche depuis le serveur proxy
    auto response = cpr::Get(cpr::Url{"http://localhost:5000/get_task"});

    if (response.status_code != 200) {
      std::cerr << "Minion: Échec lors de la récupération de la tâche."
                << std::endl;
      return 1;
    }

    // Convertir la réponse JSON en objet Task
    json task_json = json::parse(response.text);

    // Vérifier si aucune tâche n'est disponible
    if (task_json.is_null() ||
        task_json.contains("end") && task_json["end"] == true) {
      std::cout << "Minion: Plus de tâches disponibles. Arrêt." << std::endl;
      break;
    }

    Task task(task_json);
    std::cout << "Minion: Tâche " << task.identifier << " en cours"
              << std::endl;

    // Exécuter le travail
    json result = task.work();

    // Envoyer le résultat au proxy
    auto post_response =
        cpr::Post(cpr::Url{"http://localhost:8000/submit_result"},
                  cpr::Body{result.dump()},
                  cpr::Header{{"Content-Type", "application/json"}});

    if (post_response.status_code == 200) {
      std::cout << "Minion: Résultat de la tâche " << task.identifier
                << " envoyé avec succès" << std::endl;
    } else {
      std::cerr << "Minion: Échec lors de l'envoi du résultat pour la tâche "
                << task.identifier << std::endl;
    }
  }

  std::cout << "Minion: Toutes les tâches sont terminées." << std::endl;
  return 0;
}
