# 🎯 **✅ PROMPT ULTRA-COMPLÈTE POUR IA – SIMULATEUR MOOSE TEST PID (PYTHON + PYGAME)**

Crée un programme de simulation réaliste et visuelle en Python **complet**  d’un robot qui suit une ligne (blanche sur fond noir) en trajectoir de **Moose Test (évitement rapide)**, utilise **uniquement Pygame** et les bibliothèques standards (math, random). Il réagit rapidement à des changements de trajectoire comme dans un Moose Test avec un algorithme de PID. Le tout avec réglages dynamiques, deux robots en parallèle, enregistrement, affichage vectoriel, etc.

## ✅ Fonctionnalités requises :

### ➤ Robot :

* Forme : rectangle (type robot réel), avec deux roues motrices à l’arrière et une roue folle à l’avant.
Le centre de poussée est entre les roues.
* Mouvement : avance à vitesse constante (0.5–2 px/frame), la direction est régulée par le PID.
* Capteurs : 5 capteurs IR (simulés) disposés à l'avant du robot.
* Chaque capteur retourne entre 0 (sur blanc) et 1024 (sur noir).
* L’erreur est pondérée par des poids [-2, -1, 0, 1, 2] pour l’entrée PID.

### 🔁 Mouvement :

* Le robot suit automatiquement une trajectoire blanche sur fond noir.
* La trajectoire est définie par une fonction `line_path(x)`.
* Le robot est modélisé comme un carré (2 roues motrices à l’arrière + 1 roue folle à l’avant).
* Il utilise **5 capteurs IR simulés** (Analog 0-1024), espacés linéairement, pour détecter la ligne.
* Un **PID** temps réel (Kp, Ki, Kd) régule la direction du robot selon les lectures IR.

### 🎛️ Réglage dynamique :

* Raccourcis clavier pour ajuster les PID du **robot 1** :

    * `Q/A` → augmente/diminue Kp
    * `W/S` → augmente/diminue Ki
    * `E/D` → augmente/diminue Kd
* Raccourcis pour le **robot 2** (comparatif) :

    * `U/J`, `I/K`, `O/L` pour régler Kp/Ki/Kd
    * `R` → réinitialise la simulation sans perdre les PID
    * `ESC` → quitte proprement

### 📈 Visualisation intégrée :

* Affiche en haut à droite :
    * Valeur de l’erreur PID
    * Valeurs de Kp, Ki, Kd pour chaque robot
    * Rappel des touches actives
* Dessine la **trajectoire parcourue** en continu (ligne bleue et orange)
* Affiche une **courbe temps réel de l’erreur PID** intégrée dans Pygame (type oscilloscope, sans matplotlib) dans Une zone latérale dans la fenêtre (à droite). Deux courbes défilantes (erreur robot 1 & 2)
* Affiche la trajectoire parcourue du robot (ligne rouge ou colorée)
* Dessine une flèche de direction dynamique à chaque frame :
    * Proportionnelle à l’intensité de la correction PID
    * Orientée selon l’angle du robot ou erreur

### ⚙️ Spécifications techniques :

* Simulation fluide à 60 FPS
* Mémorise `error_sum` et `last_error` entre les frames
* Vitesse réaliste : 2 px/frame
* Courbes d’erreur affichées dans une zone latérale droite de l’écran

### 💾 ENREGISTREMENT :
* `F1` : Sauvegarde une capture PNG de la simulation actuelle
* `F2` : Démarre / stop l’enregistrement en .gif (imageio)
* `R` : Réinitialise le run (robot revient au départ), sans effacer les PID

### 🧠 Bonus :

* Ajoute un système de "reset" des trajectoires sans redémarrer tout
* Optimise le code (structure modulaire, performances fluides)

✅ Le code doit être **complet, structuré, commenté**, **directement exécutable**, sans bibliothèques externes (sauf Pygame).
❌ Pas de matplotlib, pas de tkinter, pas de dépendances non standards.

💡 Le rendu final doit ressembler à une vraie simulation visuelle, avec deux robots comparant leurs PID et une courbe en direct affichée dans Pygame.

```
/robot_simulation
│
├── /src
│   ├── robot.py          # Classe Robot et ses méthodes
│   ├── track.py          # Fonctions et classes pour la piste
│   ├── pid_controller.py # Classe pour le contrôleur PID
│   ├── visualization.py  # Code pour la visualisation et l'interface utilisateur
│   └── utils.py          # Fonctions utilitaires
│
├── main.py               # Point d'entrée pour exécuter la simulation
├── requirements.txt      # Dépendances du projet
└── README.md             # Documentation du projet

```