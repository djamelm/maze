class PID:
    """Contrôleur PID pour le robot"""

    def __init__(self, kp: float = 1.0, ki: float = 0.0, kd: float = 0.0, max_history: int = 100):
        self.kp, self.ki, self.kd = kp, ki, kd
        self.integral = 0.0
        # last_error=previous_error C'est la meme
        self.last_error = 0.0
        self.previous_error = 0.0
        self.error_history = []
        self.output_history = []
        self.max_history = max_history
        self.integral_limit = 100.0  # Limite pour éviter le windup

    def compute(self, error: float, sur:float) -> float:
        """
        Calcule la sortie PID

        Args:
            error (float): Erreur actuelle

        Returns:
            float: Sortie du contrôleur PID
        """

        # Calcul de la proportion
        p = self.kp * error

        # Calcul de l'intégrale avec limitation pour éviter le windup
        self.integral += error/sur
        self.integral = max(-self.integral_limit, min(self.integral_limit, self.integral))
        i = self.ki * self.integral

        # Calcul de la dérivée
        derivative = (error/sur - self.previous_error)
        d = self.kd * derivative

        # Sortie PID
        output = p + i + d

        # Mise à jour des erreurs précédentes pour le prochain calcul
        self.previous_error = error/sur
        self.last_error = error/sur

        # Historique pour affichage
        self.error_history.append(error/sur)
        if len(self.error_history) > self.max_history:
            self.error_history.pop(0)
        if len(self.output_history) > self.max_history:
            self.output_history.pop(0)
        self.output_history.append(output)
        return output

    def reset(self):
        """Remet à zéro le contrôleur PID"""
        self.integral = 0.0
        self.previous_error = 0.0
        self.last_error = 0.0
        self.error_history = []
