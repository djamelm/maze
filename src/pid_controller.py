
# Classe PID
class PID:
    """Contrôleur PID pour le robot"""
    def __init__(self, kp: float = 1.0, ki: float = 0.0, kd: float = 0.0):
        self.kp, self.ki, self.kd = kp, ki, kd
        self.integral = 0.0
        # last_error=previous_error C'est la meme
        self.last_error = 0.0
        self.previous_error = 0.0
        self.error_history = []
        
    def compute(self, error: float, dt: float = 1.0/60.0) -> float:
        """Calcule la sortie PID"""
        # Intégrale avec limitation pour éviter le windup
        self.integral += error * dt
        
        # Dérivée
        derivative = (error - self.previous_error) / dt
        
        self.last_error = error
        self.previous_error = error
        # Termes du PID
        p = self.kp * error
        i = self.ki * self.integral
        d = self.kd * derivative

        # Sortie PID
        output = p + i + d
        
        # Mémorisation pour le prochain cycle
        self.previous_error = error
        
        # Historique pour affichage
        self.error_history.append(error)
        if len(self.error_history) > self.max_history:
            self.error_history.pop(0)
            
        return output
    
    def reset(self):
        """Remet à zéro le contrôleur PID"""
        self.integral = 0.0
        self.previous_error = 0.0
        self.error_history = []