# Simulation Moose Test - Robot Suiveur de Ligne PID

Ce projet est une simulation de robots suiveurs de ligne utilisant un contrôleur PID. Les robots suivent une piste définie, et vous pouvez ajuster les paramètres PID en temps réel pour observer leur comportement.

## Table des Matières

1. [Installation](#installation)
2. [Utilisation](#utilisation)
3. [Contrôles](#contrôles)
4. [Structure du Projet](#structure-du-projet)
5. [Contribution](#contribution)
6. [Licence](#licence)
7. [Contact](#contact)

## Installation

Pour exécuter ce projet, vous aurez besoin de Python et de quelques bibliothèques supplémentaires. Voici comment les installer :

### Prérequis

- Python 3.x
- Pygame
- NumPy
- Imageio

Vous pouvez installer les bibliothèques nécessaires en utilisant pip :

```bash
python -m pip install pygame numpy imageio pyplot matplotlib
```

## Utilisation

Pour démarrer la simulation, exécutez le fichier principal main.py :

```bash
python main.py
```

## Contrôles

Voici les contrôles disponibles pour ajuster les paramètres PID des robots et interagir avec la simulation :

### Robot 1

* `Q` : Augmente Kp de 0.1
* `A` : Diminue Kp de 0.1
* `W` : Augmente Ki de 0.01
* `S` : Diminue Ki de 0.01
* `E` : Augmente Kd de 0.05
* `D` : Diminue Kd de 0.05

### Robot 2

* `U` : Augmente Kp de 0.1
* `J` : Diminue Kp de 0.1
* `I` : Augmente Ki de 0.01
* `K` : Diminue Ki de 0.01
* `O` : Augmente Kd de 0.05
* `L` : Diminue Kd de 0.05

### Général

* `R` : Réinitialise les positions des robots
* `F1` : Capture d'écran
* `F2` : Basculer l'enregistrement GIF (si activé, enregistre les images pour créer une animation GIF à la fin)
* `ESC` : Quitte la simulation

## Structure du Projet

Le projet est structuré comme suit :

```bash
project_root/
│── main.py                # Point d'entrée pour exécuter la simulation
│── configuration/
│   ├── colors.py          # Définition des couleurs utilisées dans la simulation
│   ├── robot.py           # Configuration des paramètres du robot
│   ├── screen.py          # Configuration de l'écran et paramètres d'affichage
│   └── track.py           # Configuration de la trajectoire
│── src/
│   ├── visualization.py       # Gestion de l'affichage et des graphiques
│   ├── utils.py               # Fonctions utilitaires pour la gestion des événements et des captures
│   ├── pid_controller.py  # Contrôleur PID
│   ├── robot.py           # Classe Robot et logiques associées
│   ├── track.py           # Classe Track et logiques associées
│   └── visualization.py   # Gestion de l'affichage et des graphiques
│── README.md              # Documentation du projet
```
## Contribution

Les contributions sont bienvenues ! Voici comment vous pouvez contribuer :

Fork le dépôt de projet.
Créez votre branche de fonctionnalité (git checkout -b feature/my-new-feature).
Commitez vos changements (git commit -am 'Add some feature').
Poussez vers la branche (git push origin feature/my-new-feature).
Ouvrez une Pull Request.
Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## Contact

Pour toute question ou suggestion, veuillez ouvrir une issue ou nous contacter via : djameleddine.mekki27@gmail.com.