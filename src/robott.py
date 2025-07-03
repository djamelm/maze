import pygame
import math
import random
from pid_controller import *
# Classe Robot
class Robot:
    def update(self, surface):
        error = self.get_error(surface)
        correction = self.pid.update(error)
        self.angle += correction * 0.3
        self.x += math.cos(math.radians(self.angle)) * 2
        self.y += math.sin(math.radians(self.angle)) * 2
        self.path_history.append((self.x, self.y))
        self.error_log.append(error)
        if len(self.error_log) > 300:
            self.error_log.pop(0)
            
    def update(self, track_surface: pygame.Surface):
        """Met à jour la position et l'orientation du robot"""
        # Lecture des capteurs
        self.read_sensors(track_surface)
        
        # Calcul de l'erreur
        self.current_error = self.compute_error()
        
        # Correction PID
        self.pid_output = self.pid.compute(self.current_error)
        
        # Application de la correction à l'angle
        angular_velocity = self.pid_output * 0.05  # Facteur d'échelle
        self.angle += angular_velocity
        
        # Limitation de l'angle pour éviter les rotations excessives
        self.angle = max(-math.pi/3, min(math.pi/3, self.angle))
        
        # Déplacement
        dx = self.speed * math.cos(self.angle)
        dy = self.speed * math.sin(self.angle)
        
        self.x += dx
        self.y += dy
        
        # Sauvegarde de la trajectoire
        self.path_history.append((self.x, self.y))
        if len(self.path_history) > self.max_path_history:
            self.path_history.pop(0)
                
    def update(self, line_path):
        """Met à jour la position du robot"""
        # Lecture des capteurs
        sensor_values = self.get_sensor_values(line_path)
        
        # Calcul de l'erreur pondérée
        total = 0
        weight_sum = 0
        for i in range(5):
            total += sensor_values[i] * self.sensor_weights[i]
            weight_sum += abs(self.sensor_weights[i])
        
        self.error = total / (weight_sum * 1024) * 10  # Normalisation
        
        # Calcul du PID
        steering = self.pid.compute(self.error)
        steering = max(-self.max_steering, min(steering, self.max_steering))
        
        # Mise à jour de l'orientation
        self.angle += steering
        
        # Mise à jour de la position
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)
        
        # Stockage de la trajectoire
        if len(self.path_history) < 1000:  # Limite pour éviter la surcharge
            self.path_history.append((self.x, self.y))
        
        # Calcul du vecteur direction pour l'affichage
        self.direction_vector = (
            math.cos(self.angle) * 30,
            math.sin(self.angle) * 30
        )
    def update_position(self):
        """Mise à jour de la position du robot"""
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y += self.speed * math.sin(math.radians(self.angle))
        self.get_sensor_positions()
        self.path_history.append((self.x, self.y))
        if len(self.path_history) > 500:
            self.path_history.pop(0)
            
    def update(self, surface, dt):
        """Update robot position using PID control."""
        self.error = self.read_sensors(surface)
        self.error_sum += self.error * dt
        error_diff = (self.error - self.last_error) / dt if self.last_error is not None else 0
        self.last_error = self.error

        # PID control
        correction = self.kp * self.error + self.ki * self.error_sum + self.kd * error_diff
        self.angle += correction * dt  # Adjust angle based on PID

        # Update position
        self.x += self.speed * math.cos(math.radians(self.angle)) * dt
        self.y += self.speed * math.sin(math.radians(self.angle)) * dt
        self.path.append((self.x, self.y))
        self.error_history.append(self.error)
        if len(self.error_history) > GRAPH_WIDTH:
            self.error_history.pop(0)
    def update(self, line_path):
        # Lecture des capteurs
        error = self.read_sensors(line_path)

        # Calcul du PID
        P = error
        self.error_sum += error
        I = self.error_sum
        D = error - self.last_error
        self.last_error = error

        # Calcul de la correction PID
        correction = self.Kp * P + self.Ki * I + self.Kd * D

        # Mise à jour de l'angle en fonction de la correction
        self.angle += correction * 0.01

        # Mise à jour de la position
        self.x += self.vy * math.sin(self.angle)
        self.y += self.vy * math.cos(self.angle)

        # Ajouter la position actuelle à la trajectoire
        self.path_history.append((self.x, self.y))

        # Limiter la taille de la trajectoire pour éviter une liste trop grande
        if len(self.path_history) > 1000:
            self.path_history.pop(0)

# ############################:
    def read_sensors(self, track_surface: pygame.Surface) -> List[int]:
        """Lit les capteurs IR simulés (0-1024)"""
        self.update_sensor_positions()
        values = []
        
        for pos in self.sensor_positions:
            x, y = int(pos[0]), int(pos[1])
            
            # Vérification des limites
            if 0 <= x < track_surface.get_width() and 0 <= y < track_surface.get_height():
                pixel = track_surface.get_at((x, y))
                # Conversion RGB vers valeur capteur (blanc = 0, noir = 1024)
                brightness = (pixel[0] + pixel[1] + pixel[2]) / 3
                sensor_value = int(1024 * (1 - brightness / 255))
            else:
                sensor_value = 1024  # Hors piste = noir
                
            values.append(sensor_value)
        
        self.sensor_values = values
        return values

# Robot class
# ############################:
    def read_sensors(self, surface):
        """Simulate IR sensors reading the track."""
        total_error = 0
        for i, (dx, dy) in enumerate(self.sensor_positions):
            # Transform sensor position to world coordinates
            sensor_x = self.x + dx * math.cos(math.radians(self.angle)) - dy * math.sin(math.radians(self.angle))
            sensor_y = self.y + dx * math.sin(math.radians(self.angle)) + dy * math.cos(math.radians(self.angle))
            # Check pixel color at sensor position
            try:
                color = surface.get_at((int(sensor_x), int(sensor_y)))[:3]
                # Convert color to IR reading (0 on white, 1024 on black)
                intensity = 1024 if color == BLACK else 0
                total_error += intensity * self.sensor_weights[i]
            except IndexError:
                total_error += 1024 * self.sensor_weights[i]  # Out of bounds treated as black
        return total_error / len(self.sensor_positions)

# Classe Robot
# ############################:

    def read_sensors(self, line_path):
        errors = []
        for i, pos in enumerate(self.sensor_positions):
            sensor_x = self.x + pos[0] * math.cos(self.angle) - pos[1] * math.sin(self.angle)
            sensor_y = self.y + pos[0] * math.sin(self.angle) + pos[1] * math.cos(self.angle)
            # Simuler la lecture du capteur sur la piste
            # Pour simplifier, on va supposer que la ligne est blanche (1) et le fond noir (0)
            # On vérifie si le capteur est sur la ligne
            # Ici, on utilise une fonction de distance par rapport à la ligne (simplifiée)
            distance_to_line = abs(sensor_y - line_path(sensor_x))
            # Simuler la valeur du capteur (plus proche de la ligne = plus proche de 1024)
            sensor_value = max(0, min(1024, (1 - distance_to_line / 20) * 1024))
            # Calcul de l'erreur pour ce capteur
            error = sensor_value / 1024 * self.sensor_weights[i]
            errors.append(error)
        # Calcul de l'erreur totale pondérée
        total_error = sum(errors)
        return total_error

# ############################:

    def compute_error(self) -> float:
        """Calcule l'erreur pondérée basée sur les capteurs"""
        weighted_sum = 0
        total_activation = 0
        
        for i, value in enumerate(self.sensor_values):
            # Normalisation (0-1)
            normalized_value = value / 1024.0
            weighted_sum += self.sensor_weights[i] * normalized_value
            total_activation += normalized_value
        
        # Évite la division par zéro
        if total_activation > 0.1:
            error = weighted_sum / total_activation
        else:
            error = 0.0  # Pas de ligne détectée
            
        return error