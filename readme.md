# 🎯 Simulation Moose Test - Robot Suiveur de Ligne PID

Ce projet est une simulation de robots suiveurs de ligne utilisant un contrôleur PID. Les robots suivent une piste définie (blanche sur fond noir), et vous pouvez ajuster les paramètres PID en temps réel pour observer leur comportement. Le projet inclut deux robots comparatifs, des visualisations en temps réel des courbes d'erreur, et des fonctionnalités d'enregistrement.

---

## 📋 Sommaire

1. [Fonctionnalités principales](#-fonctionnalités-principales)
1. [Installation](#-installation)
2. [Utilisation](#-utilisation)
3. [Contrôles](#-contrôles)
4. [Structure du Projet](#-structure-du-projet)
5. [Contribution](#-contribution)
6. [Licence](#-licence)
7. [Contact](#-contact)

---

## ✅ Fonctionnalités principales

- **Modélisation réaliste** : Robots rectangulaires avec 2 roues motrices arrière et 1 roue folle avant.
- **Suivi de ligne** : Détection de ligne blanche sur fond noir avec 5 capteurs IR simulés.
- **Contrôle PID** : Algorithme PID temps réel pour réguler la direction des robots.
- **Visualisation** :
  - Courbes d'erreur en temps réel (type oscilloscope)
  - Historique des trajectoires parcourues
  - Indicateur de direction dynamique
- **Comparaison en temps réel** : Deux robots avec PID configurables indépendamment.
- **Enregistrement** : Capture d'écran (PNG) et enregistrement GIF optionnel.

---

## 🔧 Installation

### Prérequis

- Python 3.x
- Pygame
- NumPy
- Imageio(pour l'enregistrement GIF)

### Installation des dépendances

Vous pouvez installer les bibliothèques nécessaires en utilisant pip :

```bash
python -m pip install pygame numpy imageio pyplot matplotlib
```
> ⚠️ **Note** : Bien que le projet utilise `imageio` pour l'enregistrement GIF, cette fonctionnalité peut être désactivée si nécessaire pour respecter les contraintes sans dépendances externes.

---

## 🚀 Utilisation

Pour démarrer la simulation, exécutez le fichier principal main.py :

```bash
python main.py
```

Le programme s'exécute à **60 FPS** avec une vitesse de déplacement de **2 pixels par frame**.

---

## ⌨️ Contrôles

Voici les contrôles disponibles pour ajuster les paramètres PID des robots et interagir avec la simulation :

| Fonctionnalité | Robot 1 | Robot 2 | Step |
|----------------|---------|---------|---------|
| **Augmenter Kp** | `Q` | `U` | 0.1 |
| **Diminuer Kp** | `A` | `J` | 0.1 |
| **Augmenter Ki** | `W` | `I` | 0.01 |
| **Diminuer Ki** | `S` | `K` | 0.01 |
| **Augmenter Kd** | `E` | `O` | 0.05 |
| **Diminuer Kd** | `D` | `L` | 0.05 |

### Général

* `R` : Réinitialise les positions des robots
* `F1` : Capture d'écran (enregistrée sous screenshot.png)
* `F2` : Basculer l'enregistrement GIF (si activé, enregistre les images pour créer une animation GIF à la fin sous le nom: simulation.gif)
* `ESC` : Quitte la simulation

---

## 🗂️ Structure du projet

```
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
│   ├── pid_controller.py  # Logique du contrôleur PID
│   ├── robot.py           # Classe Robot et logiques associées
│   ├── track.py           # Gestion du rendu de la piste
│   └── visualization.py   # Gestion de l'affichage et des graphiques
│── README.md              # Documentation du projet
```

---

## 🤝 Contribution

Les contributions sont bienvenues ! Pour contribuer :

1. Fork le dépôt
2. Créez votre branche de fonctionnalité (`git checkout -b feature/nouvelle-fonction`)
3. Committez vos modifications (`git commit -am 'Ajout de nouvelles fonctionnalités'`)
4. Poussez vers la branche (`git push origin feature/nouvelle-fonction`)
5. Ouvrez une Pull Request

---

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 📬 Contact

Pour toute question ou suggestion :
- Email : djameleddine.mekki27@gmail.com
- GitHub : [https://github.com/votre-nom/moose-test-simulator](https://github.com/votre-nom/moose-test-simulator)

---