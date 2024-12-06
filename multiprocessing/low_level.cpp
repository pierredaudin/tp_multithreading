#include <Eigen/Dense>
#include <chrono>
#include <cpr/cpr.h>
#include <iostream>
#include <nlohmann/json.hpp>

// Namespace pour JSON
using json = nlohmann::json;

int main() {
  std::cout << "Minion: Prêt à récupérer les tâches depuis le proxy"
            << std::endl;

  while (true) {
    // Récupérer une tâche depuis le proxy
    auto response = cpr::Get(cpr::Url{"http://localhost:8000"});

    if (response.status_code != 200) {
      std::cerr << "Minion: Échec lors de la récupération de la tâche."
                << std::endl;
      break;
    }

    // Convertir la réponse en JSON
    json task_json = json::parse(response.text);

    // Vérifier si aucune tâche n'est disponible
    if (task_json.is_null() ||
        (task_json.contains("end") && task_json["end"] == true)) {
      std::cout << "Minion: Plus de tâches disponibles. Arrêt." << std::endl;
      break;
    }

    // Extraire les informations de la tâche
    int identifier = task_json["identifier"];
    int size = task_json["size"];
    Eigen::MatrixXd a(size, size);
    Eigen::VectorXd b(size);

    // Charger la matrice A et le vecteur b depuis le JSON
    for (int i = 0; i < size; ++i) {
      b[i] = task_json["b"][i];
      for (int j = 0; j < size; ++j) {
        a(i, j) = task_json["a"][i][j];
      }
    }

    std::cout << "Minion: Tâche " << identifier
              << " reçue. Résolution en cours..." << std::endl;

    // Résoltution du système linéaire
    auto start = std::chrono::high_resolution_clock::now();
    Eigen::VectorXd x = a.colPivHouseholderQr().solve(
        b); //-> Le plus lent des solveurs de eigen

    // Utilisation de la décomposition LLT
    // Eigen::LLT<Eigen::MatrixXd> llt(a);
    //: Eigen::VectorXd x = llt.solve(b);

    auto end = std::chrono::high_resolution_clock::now();

    double time_taken = std::chrono::duration<double>(end - start).count();

    // Résultat en JSON
    nlohmann::json result_json;
    result_json["identifier"] = identifier;
    result_json["size"] = size;
    result_json["x"] = std::vector<double>(x.data(), x.data() + x.size());
    result_json["time"] = time_taken;

    for (int i = 0; i < size; ++i) {
      result_json["b"][i] = b[i];
      for (int j = 0; j < size; ++j) {
        result_json["a"][i][j] = a(i, j);
      }
    }

    // result_json["a"] = task_json["a"];
    // result_json["b"] = task_json["b"];

    // Envoyer le résultat au proxy
    auto post_response = cpr::Post(
        cpr::Url{"http://localhost:8000"}, cpr::Body{result_json.dump()},
        cpr::Header{{"Content-Type", "application/json"}});

    if (post_response.status_code == 200) {
      std::cout << "Minion: Résultat de la tâche " << identifier
                << " envoyé avec succès" << std::endl;
    } else {
      std::cerr << "Minion: Échec lors de l'envoi du résultat pour la tâche "
                << identifier << std::endl;
    }
  }

  std::cout << "Minion: Toutes les tâches sont terminées." << std::endl;
  return 0;
}
