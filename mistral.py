import pygame
import sys
import math
import random
import time
import os
import imageio

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulation de Robot avec PID")

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)

# Paramètres de simulation
FPS = 60
clock = pygame.time.Clock()

# Classe Robot
class Robot:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 20
        self.color = color
        self.vx = 0
        self.vy = 2  # vitesse constante
        self.angle = 0
        self.sensor_positions = [(-15, 15), (-7.5, 15), (0, 15), (7.5, 15), (15, 15)]  # positions relatives des capteurs
        self.sensor_weights = [-2, -1, 0, 1, 2]
        self.Kp = 0.5
        self.Ki = 0.0
        self.Kd = 0.1
        self.error_sum = 0
        self.last_error = 0
        self.trajectory = []

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
        self.trajectory.append((self.x, self.y))

        # Limiter la taille de la trajectoire pour éviter une liste trop grande
        if len(self.trajectory) > 1000:
            self.trajectory.pop(0)

    def draw(self, screen):
        # Dessin du robot
        robot_points = [
            (self.x + self.width / 2 * math.cos(self.angle) - self.height / 2 * math.sin(self.angle),
             self.y + self.width / 2 * math.sin(self.angle) + self.height / 2 * math.cos(self.angle)),
            (self.x + self.width / 2 * math.cos(self.angle) + self.height / 2 * math.sin(self.angle),
             self.y + self.width / 2 * math.sin(self.angle) - self.height / 2 * math.cos(self.angle)),
            (self.x - self.width / 2 * math.cos(self.angle) + self.height / 2 * math.sin(self.angle),
             self.y - self.width / 2 * math.sin(self.angle) - self.height / 2 * math.cos(self.angle)),
            (self.x - self.width / 2 * math.cos(self.angle) - self.height / 2 * math.sin(self.angle),
             self.y - self.width / 2 * math.sin(self.angle) + self.height / 2 * math.cos(self.angle))
        ]
        pygame.draw.polygon(screen, self.color, robot_points)

        # Dessin des capteurs
        for pos in self.sensor_positions:
            sensor_x = self.x + pos[0] * math.cos(self.angle) - pos[1] * math.sin(self.angle)
            sensor_y = self.y + pos[0] * math.sin(self.angle) + pos[1] * math.cos(self.angle)
            pygame.draw.circle(screen, GREEN, (int(sensor_x), int(sensor_y)), 3)

        # Dessin de la trajectoire
        if len(self.trajectory) > 1:
            pygame.draw.lines(screen, self.color, False, self.trajectory, 2)

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.error_sum = 0
        self.last_error = 0
        self.trajectory = []

# Fonction pour générer la piste
def line_path(x):
    # Générer une piste en forme de ligne avec quelques virages serrés (Moose Test)
    # On utilise une fonction sinusoïdale pour simuler des virages
    return 400 + 100 * math.sin(x / 100)

# Création des robots
robot1 = Robot(100, 400, RED)
robot2 = Robot(100, 450, BLUE)

# Fonction principale
def main():
    global robot1, robot2

    running = True
    recording = False
    frames = []

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    robot1.reset(100, 400)
                    robot2.reset(100, 450)
                elif event.key == pygame.K_F1:
                    pygame.image.save(screen, f"capture_{time.time()}.png")
                elif event.key == pygame.K_F2:
                    recording = not recording
                    if not recording and frames:
                        # Sauvegarder l'animation GIF
                        imageio.mimsave('simulation.gif', frames, fps=10)
                        frames = []

                # Ajustement des paramètres PID pour le robot 1
                elif event.key == pygame.K_q:
                    robot1.Kp += 0.1
                elif event.key == pygame.K_a:
                    robot1.Kp -= 0.1
                elif event.key == pygame.K_w:
                    robot1.Ki += 0.01
                elif event.key == pygame.K_s:
                    robot1.Ki -= 0.01
                elif event.key == pygame.K_e:
                    robot1.Kd += 0.1
                elif event.key == pygame.K_d:
                    robot1.Kd -= 0.1

                # Ajustement des paramètres PID pour le robot 2
                elif event.key == pygame.K_u:
                    robot2.Kp += 0.1
                elif event.key == pygame.K_j:
                    robot2.Kp -= 0.1
                elif event.key == pygame.K_i:
                    robot2.Ki += 0.01
                elif event.key == pygame.K_k:
                    robot2.Ki -= 0.01
                elif event.key == pygame.K_o:
                    robot2.Kd += 0.1
                elif event.key == pygame.K_l:
                    robot2.Kd -= 0.1

        # Mise à jour des robots
        robot1.update(line_path)
        robot2.update(line_path)

        # Dessin de la piste
        for x in range(0, WIDTH, 5):
            pygame.draw.circle(screen, WHITE, (x, int(line_path(x))), 2)

        # Dessin des robots
        robot1.draw(screen)
        robot2.draw(screen)

        # Affichage des paramètres PID et des informations
        font = pygame.font.SysFont(None, 24)
        pid_text1 = font.render(f"Robot 1 - Kp: {robot1.Kp:.2f}, Ki: {robot1.Ki:.2f}, Kd: {robot1.Kd:.2f}", True, WHITE)
        pid_text2 = font.render(f"Robot 2 - Kp: {robot2.Kp:.2f}, Ki: {robot2.Ki:.2f}, Kd: {robot2.Kd:.2f}", True, WHITE)
        help_text1 = font.render("Robot 1 Controls: Q/A: Kp, W/S: Ki, E/D: Kd", True, WHITE)
        help_text2 = font.render("Robot 2 Controls: U/J: Kp, I/K: Ki, O/L: Kd", True, WHITE)
        help_text3 = font.render("R: Reset, ESC: Quit, F1: Screenshot, F2: Record GIF", True, WHITE)

        screen.blit(pid_text1, (10, 10))
        screen.blit(pid_text2, (10, 40))
        screen.blit(help_text1, (10, 70))
        screen.blit(help_text2, (10, 100))
        screen.blit(help_text3, (10, 130))

        # Dessin des courbes d'erreur
        # Pour simplifier, on va dessiner un graphique simple
        # On va stocker les erreurs précédentes pour chaque robot
        if not hasattr(robot1, 'error_history'):
            robot1.error_history = []
        if not hasattr(robot2, 'error_history'):
            robot2.error_history = []

        # Ajouter la dernière erreur à l'historique
        error1 = robot1.read_sensors(line_path)
        error2 = robot2.read_sensors(line_path)
        robot1.error_history.append(error1)
        robot2.error_history.append(error2)

        # Limiter la taille de l'historique
        if len(robot1.error_history) > 200:
            robot1.error_history.pop(0)
        if len(robot2.error_history) > 200:
            robot2.error_history.pop(0)

        # Dessiner les courbes
        for i in range(1, len(robot1.error_history)):
            pygame.draw.line(screen, RED,
                             (WIDTH - 200 + i - 1, HEIGHT - 100 - robot1.error_history[i - 1] * 2),
                             (WIDTH - 200 + i, HEIGHT - 100 - robot1.error_history[i] * 2), 1)
        for i in range(1, len(robot2.error_history)):
            pygame.draw.line(screen, BLUE,
                             (WIDTH - 200 + i - 1, HEIGHT - 100 - robot2.error_history[i - 1] * 2),
                             (WIDTH - 200 + i, HEIGHT - 100 - robot2.error_history[i] * 2), 1)

        # Ajouter la frame actuelle à l'animation si on enregistre
        if recording:
            frame = pygame.surfarray.array3d(screen)
            frames.append(frame.transpose([1, 0, 2]))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
