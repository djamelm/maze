# 📚 Documentation Technique

Ce document fournit des détails techniques sur l'implémentation et les composants du projet.

## 🛠️ Architecture du Projet

Le projet est structuré pour faciliter la compréhension et la maintenance. Voici les principaux composants :

1. **Robot** : Gère la dynamique et le contrôle du robot.
2. **Piste (Track)** : Détermine le parcours que le robot doit suivre.
3. **Visualisation** : Affiche l'état actuel du robot et des données de capteurs.

## 🔄 Boucle de Contrôle

La boucle de contrôle principale s'exécute à 60 images par seconde. À chaque itération, les capteurs sont lus, le contrôleur PID calcule la correction nécessaire, et les moteurs du robot sont ajustés.

## 📊 Visualisation des Données

La simulation inclut une visualisation en temps réel des données, montrant l'erreur courante, l'historique des trajectoires, et d'autres métriques pertinentes.

## 🛠️ Outils de Développement

- **Pygame** : Utilisé pour la visualisation et l'interaction utilisateur.
- **NumPy** : Pour les calculs numériques rapides.
- **Imageio** : Utilisé optionnellement pour enregistrer des GIFs de la simulation.

---

© 2025 Moose Test Simulator
