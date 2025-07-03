import pygame
import math
from src.pid_controller import *
from configuration.colors import *
from configuration.robot import *
from src.track import *
# Classe Robot
class Robot:
    """Classe représentant un robot suiveur de ligne avec capteurs IR et contrôle PID"""
    def __init__(self, start_x= 50.0, start_y= 180.0, color= (255, 50, 50), kp=0.1, ki=0.0, kd=0.0, name='', theta=0):
        # Position et orientation
        self.x, self.y = start_x, start_y
        self.angle = theta  # angle en degres
        self.start_angle = theta  # angle en degres
        self.start_pos = (start_x, start_y)
        
        # Propriétés physiques
        self.width = ROBOT_WIDTH
        self.height = ROBOT_HEIGHT
        self.wheel_radius = 8
        self.wheel_width = 4
        self.color = color


        # Paramètres physiques
        self.speed = 2.0  # pixels par frame
        self.max_steering = 0.1  # angle de braquage max
        
        # Historique de trajectoire
        self.path_history = [(start_x, start_y)]
        self.max_path_history = 1000
        
        # Capteurs IR (5 capteurs à l'avant)
        self.sensor_count = 5
        self.sensor_spacing = 8
        # positions locales des capteurs (dans le repère du robot, origine au centre)
        self.sensor_positions_local = [
            (-self.width*0.4, self.height*0.4),
            (-self.width*0.2, self.height*0.4),
            (0,          self.height*0.4),
            (self.width*0.2,  self.height*0.4),
            (self.width*0.4,  self.height*0.4)
        ]
        self.sensor_positions=self.get_sensor_positions()
        self.sensor_values = [0,0,0,0,0]
        self.sensor_weights = [-2, -1, 0, 1, 2]  # Poids pour calcul d'erreur
        
        # Contrôleur PID
        self.Kp, self.Ki, self.Kd = kp,ki,kd
        self.pid = PID(kp, ki, kd, max_history = 100)
        self.current_error = 0.0
        self.pid_output = 0.0
        self.error_sum = 0
        self.last_error = 0
        self.error = 0
        self.error_log = []
        self.error_history = []


        self.name = name
        
        # Vectors
        self.direction_vector = (0, 0)

        self.reset()
    def update(self, track):
        """Met à jour la position et l'orientation du robot."""
        # Lecture des capteurs
        sensor_values = self.get_sensor_values(track)

        # Calcul de l'erreur pondérée
        self.current_error = self.calculate_weighted_error(sensor_values, self.sensor_weights)

        # Correction PID
        self.pid_output = self.pid.compute(self.current_error, 60)

        # Application de la correction à l'angle
        self.angle += self.pid_output

        # Mise à jour de la position
        self.update_position()
    def update_position(self):
        """Mise à jour de la position du robot."""
        self.x += self.speed * math.sin(math.radians(self.angle))
        self.y += self.speed * math.cos(math.radians(self.angle))
        self.path_history.append((self.x, self.y))
        if len(self.path_history) > self.max_path_history:
            self.path_history.pop(0)
    def reset(self):
        """Réinitialise la position du robot"""
        # Position et orientation
        self.x, self.y = self.start_pos
        self.angle = self.start_angle

        # Historique de trajectoire
        self.path_history = [(self.x, self.y)]
        self.path_history.clear()
        
        # Contrôleur PID
        self.error = 0
        self.error_sum = 0
        self.last_error = 0
        self.error_history = []
        self.pid.reset()
        self.error_log.clear()

    def draw(self, screen: pygame.Surface):
        """Dessine le robot"""
        """Affichage du robot et de ses capteurs"""
        """Draw the robot and its direction arrow."""
        """Dessine le robot sur la surface"""
        # Corps du robot (rectangle orienté)
        # Dessin du robot
        # Draw robot body
        # Création d'une surface pour le robot (pour la rotation)
        robot_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(robot_surface, self.color, (0, 0, self.width, self.height), 2, border_radius=5)
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 8)
        if len(self.path_history) > 1:
            pygame.draw.lines(screen, self.color, False, self.path_history, 2)
        # Rotation du robot
        rotated_robot = pygame.transform.rotate(robot_surface, self.angle)
        rect = rotated_robot.get_rect(center=(self.x, self.y))
        
        # Affichage
        screen.blit(rotated_robot, rect.topleft)
        
        # Dessiner les roues arrière
        wheel_width = int(self.width * 0.2)
        wheel_height = int(self.height * 0.4)

        # Position des roues
        wheel_offset_x = self.width * 0.6
        wheel_offset_y = self.height * 0.3

        # Roue gauche
        wheel_x_l = self.x - wheel_offset_x * math.cos(math.radians(-self.angle)) + wheel_offset_y * math.sin(math.radians(-self.angle))
        wheel_y_l = self.y - wheel_offset_x * math.sin(math.radians(-self.angle)) - wheel_offset_y * math.cos(math.radians(-self.angle))
        wheel_rect_l = pygame.Rect(wheel_x_l - wheel_width / 2, wheel_y_l - wheel_height / 2, wheel_width, wheel_height)

        # Roue droite
        wheel_x_r = self.x + wheel_offset_x * math.cos(math.radians(-self.angle)) + wheel_offset_y * math.sin(math.radians(-self.angle))
        wheel_y_r = self.y + wheel_offset_x * math.sin(math.radians(-self.angle)) - wheel_offset_y * math.cos(math.radians(-self.angle))
        wheel_rect_r = pygame.Rect(wheel_x_r - wheel_width / 2, wheel_y_r - wheel_height / 2, wheel_width, wheel_height)

        # Créez une surface pour chaque roue qui va être tournée
        wheel_surface_l = pygame.Surface((wheel_width, wheel_height), pygame.SRCALPHA)
        pygame.draw.rect(wheel_surface_l, GRAY, (0, 0, wheel_width, wheel_height), border_radius=3)

        wheel_surface_r = pygame.Surface((wheel_width, wheel_height), pygame.SRCALPHA)
        pygame.draw.rect(wheel_surface_r, GRAY, (0, 0, wheel_width, wheel_height), border_radius=3)

        # Faire pivoter les surfaces des roues
        rotated_wheel_l = pygame.transform.rotate(wheel_surface_l, self.angle)
        rotated_wheel_r = pygame.transform.rotate(wheel_surface_r, self.angle)

        # Trouver les nouvelles positions après rotation
        rect_l = rotated_wheel_l.get_rect(center=(wheel_x_l, wheel_y_l))
        rect_r = rotated_wheel_r.get_rect(center=(wheel_x_r, wheel_y_r))

        # Dessiner les roues sur l'écran
        screen.blit(rotated_wheel_l, rect_l)
        screen.blit(rotated_wheel_r, rect_r)


        # Dessiner la roue avant (simplifiée comme un point pour l'exemple)
        front_wheel_x = self.x + self.width/2 * math.sin(math.radians(self.angle))
        front_wheel_y = self.y + self.height*0.6/2 * math.cos(math.radians(self.angle))
        pygame.draw.circle(screen, GRAY, (int(front_wheel_x), int(front_wheel_y)), 5)
        
        
        # Capteurs (points)
        # Dessin des capteurs
        self.sensor_positions=self.get_sensor_positions()
        # Calcul de l'erreur pondérée
        for i in range(len(self.sensor_positions)):
            # Debugging: Check the type and value of `i`
            pos= self.sensor_positions[i]
            sensor_value = int(self.sensor_values[i])

            # Define color based on sensor value thresholds
            if sensor_value < 256:
                color = BLUE  # Assuming BLUE is defined
            elif 256 <= sensor_value < 512:
                color = YELLOW  # Assuming YELLOW is defined
            elif 512 <= sensor_value < 768:
                color = GREEN
            else:
                color = RED
            pygame.draw.circle(screen, color, (int(pos[0]), int(pos[1])), 3)
        
        # Trajectoire ou Chemin parcouru
        if len(self.path_history) > 1:
            pygame.draw.lines(screen, self.color, False, self.path_history, 2)
        
            #############################################


        # Direction (flèche)
        arrow_length = self.height
        arrow_end_x = self.x + arrow_length * math.sin(math.radians(self.angle))
        arrow_end_y = self.y + arrow_length * math.cos(math.radians(self.angle))
        pygame.draw.line(screen, self.color, (self.x, self.y), (arrow_end_x, arrow_end_y), 1)

        # Draw direction arrow proportional to PID correction
        arrow_length = abs(self.pid.last_error) * 0.05
        arrow_end_x = self.x + arrow_length * math.cos(math.radians(math.radians(self.angle)))
        arrow_end_y = self.y + arrow_length * math.sin(math.radians(math.radians(self.angle)))
        pygame.draw.line(screen, RED, (self.x, self.y), (arrow_end_x, arrow_end_y), 2)

        # flèche PID
        dx = math.sin(math.radians(self.angle+self.pid_output)) * 20
        dy = math.cos(math.radians(self.angle-self.pid_output)) * 20
        pygame.draw.line(screen, GREEN, (self.x, self.y), (self.x + dx, self.y + dy), 2)

    def get_sensor_values(self, track, max_distance=int(ROBOT_WIDTH*0.2)):
        """Transforme les distances en valeurs de capteurs entre 0 et 1024."""
        sensor_values = []
        distances=self.get_sensor_distances_to_track(track)
        for distance in distances:
            # Inverser la distance
            inverted_distance = max_distance - distance

            # Normaliser la distance inversée entre 0 et 1024
            sensor_value = int((inverted_distance / max_distance) * 1024)

            # Assurez-vous que la valeur est comprise entre 0 et 1024
            sensor_value = max(99, min(sensor_value, 1024))

            sensor_values.append(sensor_value)
        self.sensor_values=sensor_values
        return sensor_values
        """Récupère les valeurs des capteurs IR"""
        """Lecture des capteurs IR simulés"""

    def get_sensor_positions(self):
        sensors = []

        # convertir l'angle en radians pour le calcul trigonométrique
        theta = math.radians(-self.angle)

        # transformation locale -> globale (rotation + translation)
        for sx, sy in self.sensor_positions_local:
            # rotation
            rotated_x = sx * math.cos(theta) - sy * math.sin(theta)
            rotated_y = sx * math.sin(theta) + sy * math.cos(theta)

            # translation (ajouter position globale du robot)
            global_x = self.x + rotated_x
            global_y = self.y + rotated_y

            sensors.append((global_x, global_y))
        self.sensor_positions=sensors
        return sensors

    def calculate_weighted_error(self, sensor_values, sensor_weights):
        """
        Calcule l'erreur pondérée à partir des valeurs des capteurs.

        :param sensor_values: Liste des valeurs des capteurs.
        :param sensor_weights: Liste des poids pour chaque capteur.
        :return: Erreur pondérée.
        """
        weighted_sum = 0
        total_weight = sum(abs(weight) for weight in sensor_weights)

        for value, weight in zip(sensor_values, sensor_weights):
            weighted_sum += value * weight

        # Normaliser l'erreur pondérée
        weighted_error = weighted_sum / total_weight

        return weighted_error
    def get_error(self, surface):
        sensors = self.get_sensor_positions()
        values = []
        for sx, sy in sensors:
            try:
                color = surface.get_at((int(sx), int(sy)))[:3]
                intensity = sum(color) // 3
                value = 1024 - intensity * 4
            except IndexError:
                value = 1024
            values.append(value)
        weights = [-2, -1, 0, 1, 2]
        weighted = sum(w * v for w, v in zip(weights, values))
        total = sum(values) + 1e-6
        return weighted / total

    def distance_point_to_segment(self,point: tuple[float, float], segment_start: tuple[float, float], segment_end: tuple[float, float]) -> float:
        """Calcule la distance entre un point et un segment de ligne."""
        x, y = point
        x1, y1 = segment_start
        x2, y2 = segment_end

        # Calculer la longueur du segment au carré
        segment_length_squared = (x2 - x1) ** 2 + (y2 - y1) ** 2

        # Si le segment est un point, retourner la distance entre le point et le segment
        if segment_length_squared == 0:
            return math.sqrt((x - x1) ** 2 + (y - y1) ** 2)

        # Calculer la projection du point sur le segment
        t = max(0, min(1, ((x - x1) * (x2 - x1) + (y - y1) * (y2 - y1)) / segment_length_squared))

        # Calculer la projection
        projection_x = x1 + t * (x2 - x1)
        projection_y = y1 + t * (y2 - y1)

        # Calculer la distance entre le point et sa projection sur le segment
        return math.sqrt((x - projection_x) ** 2 + (y - projection_y) ** 2)

    def get_sensor_distances_to_track(self, track: Track):
        """Calcule la distance minimale entre chaque capteur et la piste."""
        distances = []
        track_points = track.get_track_points()

        for sensor_pos in self.sensor_positions:
            min_distance = float('inf')
            for i in range(len(track_points) - 1):
                segment_start = track_points[i]
                segment_end = track_points[i + 1]
                distance = self.distance_point_to_segment(sensor_pos, segment_start, segment_end)
                if distance < min_distance:
                    min_distance = distance
            distances.append(min_distance)
        return distances