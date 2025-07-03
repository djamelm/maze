# 🚗 Simulation Moose Test – Robot Suiveur de Ligne avec PID

Ce projet est une simulation de robots suiveurs de ligne dans un scénario de **Moose Test** (évitement rapide) utilisant un contrôleur **PID**. Les robots suivent une piste définie (blanche sur fond noir), et vous pouvez ajuster les paramètres PID en temps réel pour observer leur comportement. Le projet inclut deux robots comparatifs, des visualisations en temps réel des courbes d'erreur, et des fonctionnalités d'enregistrement.

---

## 📋 Sommaire

1. [✨ Fonctionnalités](#-fonctionnalités)
2. [🔧 Installation](#-installation)
3. [🚀 Utilisation](#-utilisation)
4. [🎮 Contrôles](#-contrôles)
5. [🗂️ Structure du Projet](#-structure-du-projet)
6. [🤝 Contribution](#-contribution)
7. [📝 Licence](#-licence)
8. [📬 Contact](#-contact)

---

## ✨ Fonctionnalités

### ➤ Robots

* Forme : Rectangle (2 roues motrices + roue folle).
* Capteurs : 5 capteurs IR simulés, lecture analogique (0–1024).
* Mouvements : Avance à vitesse constante, PID ajuste l’angle.
* Chaque capteur est pondéré : `[-2, -1, 0, 1, 2]`.

### 🔁 Trajectoire

* Ligne blanche sur fond noir,ligniare type Moose Test.

### 🎛️ Réglages PID en temps réel

* **Robot 1** : `Q/A` Kp | `W/S` Ki | `E/D` Kd
* **Robot 2** : `U/J` Kp | `I/K` Ki | `O/L` Kd

### 📈 Visualisation intégrée

* Valeurs Kp, Ki, Kd affichées.
* Courbes en direct des erreurs PID (oscilloscope intégré Pygame).
* Dessin des trajectoires parcourues.
* Flèches directionnelles selon l’erreur PID.

### 💾 Enregistrement

* `F1` : Capture PNG
* `F2` : Toggle enregistrement GIF (via `imageio`)
* `R` : Réinitialisation simulation (sans réinitialiser les PID)

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

## 🎮 Contrôles

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

| Touche | Action                                |
| ------ | ------------------------------------- |
| `R`    | Réinitialise les positions des robots          |
| `F1`   | Sauvegarde screenshot PNG             |
| `F2`   | Démarrer / arrêter enregistrement GIF |
| `ESC`  | Quitter la simulation                 |

---

## 🗂️ Structure du Projet

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

Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le dépôt
2. Créez votre branche de fonctionnalité (`git checkout -b feature/nouvelle-fonction`)
3. Committez vos modifications (`git commit -am 'Ajout de nouvelles fonctionnalités'`)
4. Poussez vers la branche (`git push origin feature/nouvelle-fonction`)
5. Ouvrez une Pull Request

---

## 📝 Licence

Ce projet est sous licence **MIT** - voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 📬 Contact

Pour toute question ou suggestion :

> ✉️ Email : [djameleddine.mekki27@gmail.com](mailto:djameleddine.mekki27@gmail.com)

> 🔗 GitHub : [@djamelm](https://github.com/djamelm)

---