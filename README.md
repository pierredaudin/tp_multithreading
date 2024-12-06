# README: Résultats Benchmark solvers

## Solvers et Langages

### Langages
- **C++**
  - Solveurs testés:
    - `ColPivHouseholderQR`
    - `LLT`
- **Python**
  - Solveur testé:
    - Numpy's `linalg.solve`

---

## Resultats

| Taille | Langage | Solveur                  |  Temps total pour 10 tâches (en s) |
|-------------|----------|-------------------------|------------------|
| \( 10 	imes 10 \) | C++      | ColPivHouseholderQR      | 1.32e-04       |
| \( 10 	imes 10 \) | C++      | LLT                     | 5.293e-05       |
| \( 10 	imes 10 \) | Python   | linalg.solve            | 4.794e-04       |
| \( 1000 	imes 1000 \) | C++      | ColPivHouseholderQR      | 1.582          |
| \( 1000 	imes 1000 \) | C++      | LLT                     | 3.557e-05          |
| \( 1000 	imes 1000 \) | Python   | linalg.solve            | 3.629e-04          |

---

## Conclusion
- `LLT` est plus performant que `ColPivHouseholderQR` pour le c++ et que `linalg.solve` pour le python.
- `ColPivHouseholderQR` est plus rapide que `linalg.solve` quand la taille est à 10 mais quand on l'augmente à 1000, `ColPivHouseholderQR` est beaucoup plus lent tandis que `linalg.solve` garde les mêmes performances.
- En focntion du solver utilisé, python peut être plus rapide que c++ et inversement.
