# 🚀 Explication du Contrôleur PID

Ce document explique comment fonctionne le contrôleur PID utilisé dans la simulation du robot suiveur de ligne.

## 📘 Qu'est-ce qu'un PID ?

Le contrôleur PID (Proportionnel, Intégral, Dérivé) est un mécanisme de contrôle en boucle fermée largement utilisé dans les systèmes de contrôle automatisé. Il permet de réguler une variable de processus pour obtenir une valeur souhaitée.

## 📌 Composantes du PID

1. **Proportionnel (Kp)** : Répond à l'erreur actuelle. Un gain proportionnel élevé peut rendre le système plus réactif mais peut aussi causer des oscillations.

2. **Intégral (Ki)** : Compense les erreurs passées. Cela aide à éliminer l'erreur résiduelle mais peut conduire à une surcompensation si le gain est trop élevé.

3. **Dérivé (Kd)** : Prédit les erreurs futures en fonction du taux de changement actuel. Cela peut réduire l'overshoot et améliorer la stabilité, mais il peut être sensible au bruit.

## 🔍 Savoir quand et comment changer les paramètres PID

### Comment ajuster Kp, Ki, et Kd ?

1. **Kp (Gain Proportionnel) :**
   - **Symptôme de réglage incorrect** : Si Kp est trop élevé, le système peut devenir instable et osciller autour de la valeur désirée. Si Kp est trop bas, le système peut être lent à répondre aux changements.
   - **Comment ajuster** : Commencez par augmenter Kp jusqu'à ce que le système commence à osciller, puis réduisez légèrement pour atteindre un bon compromis entre rapidité et stabilité.

2. **Ki (Gain Intégral) :**
   - **Symptôme de réglage incorrect** : Si Ki est trop élevé, le système peut osciller ou surcompenser. Si Ki est trop bas, il peut prendre trop de temps pour corriger les erreurs, ou ne jamais les corriger complètement.
   - **Comment ajuster** : Augmentez Ki jusqu'à ce que l'erreur résiduelle soit éliminée, mais faites attention aux oscillations. Un bon réglage de Ki peut éliminer les erreurs persistantes.

3. **Kd (Gain Dérivé) :**
   - **Symptôme de réglage incorrect** : Si Kd est trop élevé, le système peut devenir très rigide et sensible au bruit. Si Kd est trop bas, le système peut être lent à corriger les tendances changeantes.
   - **Comment ajuster** : Réglez Kd pour atténuer les oscillations causées par Kp et Ki. Un bon réglage de Kd peut améliorer la stabilité et réduire les excès de réponse.

### Techniques de Réglage

- **Méthode de Ziegler-Nichols** : Une méthode classique pour régler les paramètres PID. Commencez par mettre Ki et Kd à zéro et augmentez Kp jusqu'à ce que le système commence à osciller à une fréquence constante (appelée la limite de stabilité). Notez la valeur de Kp à ce point, appelée Ku, et la période d'oscillation, appelée Pu. Ziegler-Nichols propose alors des réglages pour Kp, Ki et Kd en fonction de Ku et Pu.

- **Essais et Erreurs** : Dans de nombreux cas, surtout pour les systèmes simples ou simulés, ajuster manuellement chaque paramètre tout en observant le comportement du système peut être très efficace.

- **Observation du Comportement** : Pendant le réglage, observez comment le robot se comporte sur la piste. Vous voulez une réponse rapide mais stable qui suit la ligne avec précision.

### Conseils Pratiques

- **Commencez par Kp** : Stabilisez d'abord la réponse avec Kp avant de toucher à Ki et Kd.
- **Utilisez Ki pour éliminer les erreurs stables** : Si le robot ne suit pas parfaitement la ligne après avoir réglé Kp, Ki peut aider à corriger cette erreur continue.
- **Utilisez Kd pour réduire les oscillations** : Si le robot oscille autour de la ligne, Kd peut aider à stabiliser le système.

En ajustant ces paramètres, vous pouvez optimiser la performance du robot pour qu'il suive la ligne de manière rapide et stable sans oscillations excessives.


## 🛠️ Utilisation dans le Projet

Dans notre projet, le PID est utilisé pour ajuster la direction du robot de manière à minimiser l'écart entre sa position actuelle et la ligne qu'il est censé suivre. Les gains Kp, Ki, et Kd peuvent être ajustés en temps réel pour observer leur effet sur le comportement du robot.

## ⚙️ Configuration

Les gains peuvent être ajustés via l'interface de la simulation en utilisant les touches suivantes :

- `Q`/`A` : Augmenter/diminuer Kp pour le Robot 1
- `W`/`S` : Augmenter/diminuer Ki pour le Robot 1
- `E`/`D` : Augmenter/diminuer Kd pour le Robot 1

Pour le Robot 2, utilisez `U`, `I`, `O` pour augmenter et `J`, `K`, `L` pour diminuer respectivement.

## 🌟 Optimisation des Réglages

Pour obtenir une réponse optimale, commencez par régler Kp jusqu'à ce que le système réponde rapidement sans oscillation excessive. Ensuite, ajustez Ki pour éliminer les erreurs à l'état stable. Enfin, réglez Kd pour améliorer la stabilité en cas de variations rapides.

---

© 2025 Moose Test Simulator
