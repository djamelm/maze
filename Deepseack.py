import pygame
import math
import random
import sys
from pygame import gfxdraw

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
WIDTH, HEIGHT = 1200, 700
TRACK_WIDTH = WIDTH - 300  # Largeur de la zone de simulation
GRAPH_WIDTH = 300         # Largeur de la zone de graphique

# Création de la fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚗 Moose Test - Robot Suiveur de Ligne PID")

# Couleurs
BACKGROUND = (10, 10, 30)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 100)
BLUE = (50, 150, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 150, 50)
PURPLE = (180, 70, 220)
LIGHT_BLUE = (100, 200, 255)
LIGHT_RED = (255, 100, 100)
TRACK_COLOR = (60, 60, 80)
LINE_COLOR = (220, 220, 255)

# Police
font = pygame.font.SysFont('Arial', 18)
title_font = pygame.font.SysFont('Arial', 28, bold=True)

class PIDController:
    """Contrôleur PID pour le suivi de ligne"""
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.error_sum = 0
        self.last_error = 0
    
    def compute(self, error, dt=1.0):
        """Calcule la sortie du PID"""
        self.error_sum += error * dt
        derivative = (error - self.last_error) / dt if dt > 0 else 0
        self.last_error = error
        
        # Termes du PID
        p = self.kp * error
        i = self.ki * self.error_sum
        d = self.kd * derivative
        
        return p + i + d

class Robot:
    """Robot suiveur de ligne avec capteurs IR et contrôle PID"""
    def __init__(self, x, y, theta=0, color=GREEN, pid_params=(0.1, 0.001, 0.05)):
        # Position et orientation
        self.x = x
        self.y = y
        self.theta = theta  # angle en radians
        
        # Dimensions du robot
        self.width = 40
        self.height = 20
        self.wheel_radius = 8
        self.wheel_width = 4
        
        # Paramètres physiques
        self.speed = 1.8  # vitesse en px/frame
        self.max_steering = 0.1  # angle de braquage max
        
        # Capteurs IR
        self.sensor_positions = [
            (-self.width*0.4, -self.height*0.8),
            (-self.width*0.2, -self.height*0.8),
            (0, -self.height*0.8),
            (self.width*0.2, -self.height*0.8),
            (self.width*0.4, -self.height*0.8)
        ]
        self.sensor_weights = [-2, -1, 0, 1, 2]
        
        # PID
        self.pid = PIDController(*pid_params)
        self.error = 0
        self.color = color
        self.trajectory = []
        
        # Pour l'affichage
        self.direction_vector = (0, 0)
    
    def get_sensor_values(self, line_path):
        """Récupère les valeurs des capteurs IR"""
        values = []
        for dx, dy in self.sensor_positions:
            # Position absolue du capteur
            sensor_x = self.x + dx * math.cos(self.theta) - dy * math.sin(self.theta)
            sensor_y = self.y + dx * math.sin(self.theta) + dy * math.cos(self.theta)
            
            # Calcul de la valeur du capteur (0=blanc, 1024=noir)
            line_y = line_path(sensor_x)
            distance = abs(sensor_y - line_y)
            
            # Plus le capteur est proche de la ligne, plus la valeur est élevée
            value = max(0, 1024 - distance * 10)
            values.append(value)
        
        return values
    
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
        self.theta += steering
        
        # Mise à jour de la position
        self.x += self.speed * math.cos(self.theta)
        self.y += self.speed * math.sin(self.theta)
        
        # Stockage de la trajectoire
        if len(self.trajectory) < 1000:  # Limite pour éviter la surcharge
            self.trajectory.append((self.x, self.y))
        
        # Calcul du vecteur direction pour l'affichage
        self.direction_vector = (
            math.cos(self.theta) * 30,
            math.sin(self.theta) * 30
        )
    
    def reset(self, x, y, theta):
        """Réinitialise la position du robot"""
        self.x = x
        self.y = y
        self.theta = theta
        self.pid.error_sum = 0
        self.pid.last_error = 0
        self.trajectory = []
    
    def draw(self, surface):
        """Dessine le robot sur la surface"""
        # Dessin de la trajectoire
        if len(self.trajectory) > 1:
            pygame.draw.lines(surface, self.color, False, self.trajectory, 2)
        
        # Création d'une surface pour le robot (pour la rotation)
        robot_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(robot_surface, self.color, (0, 0, self.width, self.height), 2, border_radius=5)
        
        # Roues arrière
        pygame.draw.rect(robot_surface, (100, 100, 120), 
                        (self.width*0.1, self.height*0.2, self.width*0.8, self.height*0.6), 
                        border_radius=3)
        
        # Roue avant
        pygame.draw.circle(robot_surface, (100, 100, 120), 
                          (int(self.width/2), int(self.height*0.8)), 5)
        
        # Capteurs
        for i, (dx, dy) in enumerate(self.sensor_positions):
            pygame.draw.circle(robot_surface, LIGHT_RED if i == 2 else RED, 
                              (int(self.width/2 + dx), int(self.height/2 + dy)), 3)
        
        # Rotation du robot
        rotated_robot = pygame.transform.rotate(robot_surface, -math.degrees(self.theta))
        rect = rotated_robot.get_rect(center=(self.x, self.y))
        
        # Affichage
        surface.blit(rotated_robot, rect.topleft)
        
        # Flèche de direction
        end_x = self.x + self.direction_vector[0]
        end_y = self.y + self.direction_vector[1]
        pygame.draw.line(surface, YELLOW, (self.x, self.y), (end_x, end_y), 2)
        pygame.draw.circle(surface, YELLOW, (int(end_x), int(end_y)), 4)

def moose_test_path(x):
    """Définit la trajectoire du Moose Test"""
    # Ligne droite initiale
    if x < 200:
        return HEIGHT // 2
    
    # Premier virage
    elif x < 350:
        return HEIGHT // 2 - 80 * math.sin((x - 200) * math.pi / 300)
    
    # Deuxième virage (contre-manœuvre)
    elif x < 500:
        return HEIGHT // 2 - 80 * math.sin((350 - 200) * math.pi / 300) + 120 * math.sin((x - 350) * math.pi / 300)
    
    # Troisième virage
    elif x < 650:
        return HEIGHT // 2 - 80 * math.sin((350 - 200) * math.pi / 300) + 120 * math.sin((500 - 350) * math.pi / 300) - 80 * math.sin((x - 500) * math.pi / 300)
    
    # Retour à la ligne droite
    else:
        return HEIGHT // 2

def draw_pid_graph(surface, errors1, errors2, x, y, width, height):
    """Dessine le graphique PID"""
    # Cadre du graphique
    pygame.draw.rect(surface, (40, 40, 60), (x, y, width, height))
    pygame.draw.rect(surface, (100, 100, 150), (x, y, width, height), 2)
    
    # Titre
    title = title_font.render("Erreur PID", True, LIGHT_BLUE)
    surface.blit(title, (x + width//2 - title.get_width()//2, y + 10))
    
    # Lignes de grille
    for i in range(1, 5):
        pygame.draw.line(surface, (60, 60, 80), 
                        (x, y + i * height//5), 
                        (x + width, y + i * height//5), 1)
    
    # Axe central (zéro)
    pygame.draw.line(surface, (100, 100, 150), 
                    (x, y + height//2), 
                    (x + width, y + height//2), 1)
    
    # Courbe d'erreur pour le robot 1
    if len(errors1) > 1:
        points = []
        for i, error in enumerate(errors1):
            px = x + width - (len(errors1) - i) * 2
            py = y + height//2 - error * height//3
            points.append((px, py))
        
        pygame.draw.lines(surface, GREEN, False, points, 2)
    
    # Courbe d'erreur pour le robot 2
    if len(errors2) > 1:
        points = []
        for i, error in enumerate(errors2):
            px = x + width - (len(errors2) - i) * 2
            py = y + height//2 - error * height//3
            points.append((px, py))
        
        pygame.draw.lines(surface, BLUE, False, points, 2)
    
    # Légendes
    pygame.draw.line(surface, GREEN, (x + 20, y + height - 30), (x + 50, y + height - 30), 2)
    pygame.draw.line(surface, BLUE, (x + 20, y + height - 10), (x + 50, y + height - 10), 2)
    
    text1 = font.render("Robot 1", True, GREEN)
    text2 = font.render("Robot 2", True, BLUE)
    surface.blit(text1, (x + 60, y + height - 35))
    surface.blit(text2, (x + 60, y + height - 15))

def draw_control_panel(surface, robot1, robot2, x, y):
    """Dessine le panneau de contrôle"""
    pygame.draw.rect(surface, (30, 30, 50), (x, y, GRAPH_WIDTH - 20, 240))
    pygame.draw.rect(surface, (80, 80, 120), (x, y, GRAPH_WIDTH - 20, 240), 2)
    
    # Titre
    title = title_font.render("Paramètres PID", True, LIGHT_BLUE)
    surface.blit(title, (x + (GRAPH_WIDTH - 20)//2 - title.get_width()//2, y + 10))
    
    # Paramètres Robot 1
    y_offset = y + 50
    pygame.draw.rect(surface, (40, 40, 60), (x + 10, y_offset, GRAPH_WIDTH - 40, 80), 0, 5)
    pygame.draw.rect(surface, GREEN, (x + 10, y_offset, GRAPH_WIDTH - 40, 80), 2, 5)
    
    title1 = font.render("ROBOT 1", True, GREEN)
    surface.blit(title1, (x + (GRAPH_WIDTH - 20)//2 - title1.get_width()//2, y_offset + 5))
    
    kp_text = font.render(f"Kp: {robot1.pid.kp:.3f} (Q/A)", True, WHITE)
    ki_text = font.render(f"Ki: {robot1.pid.ki:.5f} (W/S)", True, WHITE)
    kd_text = font.render(f"Kd: {robot1.pid.kd:.3f} (E/D)", True, WHITE)
    
    surface.blit(kp_text, (x + 20, y_offset + 25))
    surface.blit(ki_text, (x + 20, y_offset + 45))
    surface.blit(kd_text, (x + 20, y_offset + 65))
    
    # Paramètres Robot 2
    y_offset += 100
    pygame.draw.rect(surface, (40, 40, 60), (x + 10, y_offset, GRAPH_WIDTH - 40, 80), 0, 5)
    pygame.draw.rect(surface, BLUE, (x + 10, y_offset, GRAPH_WIDTH - 40, 80), 2, 5)
    
    title2 = font.render("ROBOT 2", True, BLUE)
    surface.blit(title2, (x + (GRAPH_WIDTH - 20)//2 - title2.get_width()//2, y_offset + 5))
    
    kp_text = font.render(f"Kp: {robot2.pid.kp:.3f} (U/J)", True, WHITE)
    ki_text = font.render(f"Ki: {robot2.pid.ki:.5f} (I/K)", True, WHITE)
    kd_text = font.render(f"Kd: {robot2.pid.kd:.3f} (O/L)", True, WHITE)
    
    surface.blit(kp_text, (x + 20, y_offset + 25))
    surface.blit(ki_text, (x + 20, y_offset + 45))
    surface.blit(kd_text, (x + 20, y_offset + 65))
    
    # Commandes
    y_offset += 100
    controls = [
        "R: Réinitialiser la simulation",
        "F1: Capture d'écran",
        "ESC: Quitter"
    ]
    
    for i, text in enumerate(controls):
        ctrl = font.render(text, True, YELLOW)
        surface.blit(ctrl, (x + 20, y_offset + i*25))

def draw_track(surface, line_path):
    """Dessine la piste avec la ligne à suivre"""
    # Fond de piste
    pygame.draw.rect(surface, TRACK_COLOR, (0, 0, TRACK_WIDTH, HEIGHT))
    
    # Ligne à suivre
    points = []
    for x in range(0, TRACK_WIDTH, 5):
        y = line_path(x)
        points.append((x, y))
    
    if len(points) > 1:
        pygame.draw.lines(surface, LINE_COLOR, False, points, 5)
    
    # Bordure de piste
    pygame.draw.line(surface, (100, 100, 150), (TRACK_WIDTH, 0), (TRACK_WIDTH, HEIGHT), 3)

def main():
    # Création des robots
    robot1 = Robot(50, HEIGHT // 2, 0, GREEN, (0.12, 0.0008, 0.08))
    robot2 = Robot(50, HEIGHT // 2 - 40, 0, BLUE, (0.10, 0.0005, 0.06))
    
    # Historique des erreurs
    errors1 = []
    errors2 = []
    
    # Variables pour l'enregistrement
    recording = False
    frame_count = 0
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Gestion du clavier
            if event.type == pygame.KEYDOWN:
                # Réglages PID robot1
                if event.key == pygame.K_q:  # Kp +
                    robot1.pid.kp += 0.01
                elif event.key == pygame.K_a:  # Kp -
                    robot1.pid.kp = max(0, robot1.pid.kp - 0.01)
                elif event.key == pygame.K_w:  # Ki +
                    robot1.pid.ki += 0.0001
                elif event.key == pygame.K_s:  # Ki -
                    robot1.pid.ki = max(0, robot1.pid.ki - 0.0001)
                elif event.key == pygame.K_e:  # Kd +
                    robot1.pid.kd += 0.01
                elif event.key == pygame.K_d:  # Kd -
                    robot1.pid.kd = max(0, robot1.pid.kd - 0.01)
                
                # Réglages PID robot2
                elif event.key == pygame.K_u:  # Kp +
                    robot2.pid.kp += 0.01
                elif event.key == pygame.K_j:  # Kp -
                    robot2.pid.kp = max(0, robot2.pid.kp - 0.01)
                elif event.key == pygame.K_i:  # Ki +
                    robot2.pid.ki += 0.0001
                elif event.key == pygame.K_k:  # Ki -
                    robot2.pid.ki = max(0, robot2.pid.ki - 0.0001)
                elif event.key == pygame.K_o:  # Kd +
                    robot2.pid.kd += 0.01
                elif event.key == pygame.K_l:  # Kd -
                    robot2.pid.kd = max(0, robot2.pid.kd - 0.01)
                
                # Commandes générales
                elif event.key == pygame.K_r:  # Reset
                    robot1.reset(50, HEIGHT // 2, 0)
                    robot2.reset(50, HEIGHT // 2 - 40, 0)
                    errors1 = []
                    errors2 = []
                elif event.key == pygame.K_F1:  # Capture d'écran
                    pygame.image.save(screen, "moose_test_simulation.png")
                elif event.key == pygame.K_ESCAPE:  # Quitter
                    running = False
        
        # Mise à jour des robots
        robot1.update(moose_test_path)
        robot2.update(moose_test_path)
        
        # Mise à jour des erreurs
        errors1.append(robot1.error)
        errors2.append(robot2.error)
        
        # Limite la taille des historiques
        if len(errors1) > 200:
            errors1.pop(0)
        if len(errors2) > 200:
            errors2.pop(0)
        
        # Dessin
        screen.fill(BACKGROUND)
        
        # Piste et ligne
        draw_track(screen, moose_test_path)
        
        # Robots
        robot1.draw(screen)
        robot2.draw(screen)
        
        # Graphique PID
        draw_pid_graph(screen, errors1, errors2, TRACK_WIDTH, 0, GRAPH_WIDTH, HEIGHT // 2)
        
        # Panneau de contrôle
        draw_control_panel(screen, robot1, robot2, TRACK_WIDTH, HEIGHT // 2 + 20)
        
        # Titre principal
        title = title_font.render("Simulation Moose Test - Robot Suiveur de Ligne PID", True, YELLOW)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 10))
        
        # Informations
        info_text = font.render("Utilisez les touches pour ajuster les paramètres PID en temps réel", True, LIGHT_BLUE)
        screen.blit(info_text, (WIDTH // 2 - info_text.get_width() // 2, HEIGHT - 30))
        
        # Mise à jour de l'affichage
        pygame.display.flip()
        
        # Contrôle de la vitesse de la simulation
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()