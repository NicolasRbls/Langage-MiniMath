# Langage MiniMath

Langage MiniMath est un langage minimaliste permettant d’exécuter des opérations arithmétiques et d’afficher des résultats. Ce projet comprend un **compilateur**, un **interpréteur**, et des **exemples de code**.

## Fonctionnalités
- Compilation de programmes MiniMath en fichier binaire
- Interprétation et exécution des fichiers binaires compilés
- Opérations arithmétiques (`+`, `-`, `*`, `/`)
- Manipulation de variables et affichage avec `ecrire()`
- Support des tableaux et des chaînes de caractères

## Architecture du projet
```
Langage-MiniMath/
├── interprete_minimath.py   # Interpréteur du langage MiniMath
├── minimath_compiler.py     # Compilateur du langage MiniMath
├── test.mm                  # Exemple de code MiniMath
├── output.bin               # Fichier binaire généré après compilation
└── README.md                # Documentation du projet
```

## Installation et Prérequis
### 1. Cloner le dépôt
```sh
git clone https://github.com/ton-utilisateur/Langage-MiniMath.git
cd Langage-MiniMath
```

### 2. Vérifier l’installation de Python
```sh
python --version
```

## Utilisation
### Compiler un programme MiniMath
Exemple de code MiniMath (`test.mm`) :
```mm
x = 10
y = 20
z = x + y
ecrire(z)

tableau = [5, 10, 15]
ecrire(tableau)
ecrire("Fin-du-programme")
```
Pour compiler ce fichier :
```sh
python minimath_compiler.py test.mm
```
Cela génère un fichier `output.bin`.

### Exécuter un programme compilé
```sh
python interprete_minimath.py
```
**Sortie attendue :**
```
30
[5, 10, 15]
Fin-du-programme
```

## Explication des fichiers
- `minimath_compiler.py` : Tokenise et parse le code MiniMath puis génère un fichier binaire `output.bin`.
- `interprete_minimath.py` : Lit et exécute le fichier `output.bin`.
- `test.mm` : Exemple de programme MiniMath.

## Exemples d'Instructions
| Instruction | Fonction |
|-------------|----------------------------------|
| `x = 10` | Stocke 10 dans `x` |
| `y = x + 5` | Additionne `x` avec 5 et stocke le résultat dans `y` |
| `ecrire(y)` | Affiche la valeur de `y` |
| `tableau = [1, 2, 3]` | Définit un tableau |
| `ecrire(tableau)` | Affiche `[1, 2, 3]` |

## Améliorations Futures
- Ajout des boucles `while` et conditions `if`
- Gestion avancée des types (booléens, flottants)
- Amélioration du système d'erreurs et debug

## Licence
Ce projet est sous licence **MIT** - Libre d’utilisation et de modification.

---

**Auteur** : *Nicolas, Badre*  

