#!/usr/bin/env python3
"""
Simulateur Moose Test PID - Robot suiveur de ligne
Simulation réaliste avec contrôle PID, visualisation temps réel et comparaison de deux robots
"""

import pygame
import math
import random
import time
import os
from typing import Tuple, List, Optional

# Initialisation de Pygame
pygame.init()

# Constantes
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
TRACK_WIDTH = 800
INFO_PANEL_WIDTH = SCREEN_WIDTH - TRACK_WIDTH
FPS = 60

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)

class PIDController:
    """Contrôleur PID pour le robot"""
    
    def __init__(self, kp: float = 1.0, ki: float = 0.0, kd: float = 0.0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral = 0.0
        self.previous_error = 0.0
        self.error_history = []
        self.max_history = 300  # 5 secondes à 60 FPS
        
    def compute(self, error: float, dt: float = 1.0/60.0) -> float:
        """Calcule la sortie PID"""
        # Intégrale avec limitation pour éviter le windup
        self.integral += error * dt
        self.integral = max(-10, min(10, self.integral))  # Limitation
        
        # Dérivée
        derivative = (error - self.previous_error) / dt
        
        # Sortie PID
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        
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

class Robot:
    """Classe représentant un robot suiveur de ligne"""
    
    def __init__(self, start_x: float, start_y: float, color: Tuple[int, int, int], name: str):
        # Position et orientation
        self.x = start_x
        self.y = start_y
        self.angle = 0.0  # Angle en radians
        self.color = color
        self.name = name
        
        # Propriétés physiques
        self.width = 30
        self.height = 20
        self.speed = 2.0  # pixels par frame
        
        # Capteurs IR (5 capteurs à l'avant)
        self.sensor_count = 5
        self.sensor_spacing = 8
        self.sensor_positions = []
        self.sensor_values = [0] * self.sensor_count
        self.sensor_weights = [-2, -1, 0, 1, 2]  # Poids pour calcul d'erreur
        
        # Contrôleur PID
        self.pid = PIDController(kp=1.5, ki=0.01, kd=0.5)
        
        # Historique de trajectoire
        self.path_history = []
        self.max_path_history = 1000
        
        # État
        self.current_error = 0.0
        self.pid_output = 0.0
        
    def update_sensor_positions(self):
        """Met à jour les positions des capteurs par rapport au robot"""
        self.sensor_positions = []
        
        # Capteurs alignés à l'avant du robot
        for i in range(self.sensor_count):
            offset_x = (i - 2) * self.sensor_spacing  # Centré sur le capteur du milieu
            offset_y = -self.height // 2  # À l'avant du robot
            
            # Rotation selon l'angle du robot
            rotated_x = offset_x * math.cos(self.angle) - offset_y * math.sin(self.angle)
            rotated_y = offset_x * math.sin(self.angle) + offset_y * math.cos(self.angle)
            
            sensor_x = self.x + rotated_x
            sensor_y = self.y + rotated_y
            
            self.sensor_positions.append((sensor_x, sensor_y))
    
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
    
    def draw(self, surface: pygame.Surface):
        """Dessine le robot"""
        # Corps du robot (rectangle orienté)
        corners = []
        for dx, dy in [(-self.width//2, -self.height//2), (self.width//2, -self.height//2),
                      (self.width//2, self.height//2), (-self.width//2, self.height//2)]:
            rotated_x = dx * math.cos(self.angle) - dy * math.sin(self.angle)
            rotated_y = dx * math.sin(self.angle) + dy * math.cos(self.angle)
            corners.append((self.x + rotated_x, self.y + rotated_y))
        
        pygame.draw.polygon(surface, self.color, corners)
        
        # Direction (flèche)
        arrow_length = 25
        arrow_end_x = self.x + arrow_length * math.cos(self.angle)
        arrow_end_y = self.y + arrow_length * math.sin(self.angle)
        pygame.draw.line(surface, WHITE, (self.x, self.y), (arrow_end_x, arrow_end_y), 3)
        
        # Capteurs (points)
        for pos in self.sensor_positions:
            pygame.draw.circle(surface, GREEN, (int(pos[0]), int(pos[1])), 3)
        
        # Trajectoire
        if len(self.path_history) > 1:
            pygame.draw.lines(surface, self.color, False, self.path_history, 2)
    
    def reset_position(self, start_x: float, start_y: float):
        """Remet le robot à sa position de départ"""
        self.x = start_x
        self.y = start_y
        self.angle = 0.0
        self.path_history = []
        self.pid.reset()

class MooseTestTrack:
    """Générateur de piste Moose Test"""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.line_width = 40
        
    def generate_track(self) -> pygame.Surface:
        """Génère la piste de Moose Test"""
        surface = pygame.Surface((self.width, self.height))
        surface.fill(BLACK)
        
        # Ligne blanche avec trajectoire Moose Test
        points = []
        for x in range(0, self.width, 2):
            y = self.moose_test_function(x)
            points.append((x, y))
        
        # Dessine la ligne épaisse
        if len(points) > 1:
            for i in range(len(points) - 1):
                pygame.draw.line(surface, WHITE, points[i], points[i + 1], self.line_width)
        
        return surface
    
    def moose_test_function(self, x: float) -> float:
        """Fonction mathématique du Moose Test"""
        center_y = self.height // 2
        
        # Phase 1: ligne droite
        if x < 150:
            return center_y
        
        # Phase 2: évitement rapide (S-curve)
        elif x < 300:
            progress = (x - 150) / 150
            amplitude = 120
            return center_y + amplitude * math.sin(progress * math.pi * 2)
        
        # Phase 3: retour au centre avec oscillations
        elif x < 500:
            progress = (x - 300) / 200
            amplitude = 80 * (1 - progress)
            frequency = 3
            return center_y + amplitude * math.sin(progress * math.pi * frequency)
        
        # Phase 4: ligne droite finale
        else:
            return center_y

class ErrorGraph:
    """Graphique d'erreur temps réel"""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.max_points = 300
        
    def draw(self, surface: pygame.Surface, robot1: Robot, robot2: Robot):
        """Dessine le graphique d'erreur"""
        # Fond
        pygame.draw.rect(surface, DARK_GRAY, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)
        
        # Ligne centrale (erreur = 0)
        center_y = self.rect.centery
        pygame.draw.line(surface, GRAY, (self.rect.left, center_y), (self.rect.right, center_y), 1)
        
        # Courbes d'erreur
        self.draw_error_curve(surface, robot1.pid.error_history, BLUE, "Robot 1")
        self.draw_error_curve(surface, robot2.pid.error_history, ORANGE, "Robot 2")
        
        # Titre
        font = pygame.font.Font(None, 24)
        title = font.render("Erreur PID", True, WHITE)
        surface.blit(title, (self.rect.x + 5, self.rect.y + 5))
    
    def draw_error_curve(self, surface: pygame.Surface, error_history: List[float], color: Tuple[int, int, int], label: str):
        """Dessine une courbe d'erreur"""
        if len(error_history) < 2:
            return
        
        points = []
        for i, error in enumerate(error_history):
            x = self.rect.left + (i / self.max_points) * self.rect.width
            # Normalisation de l'erreur (-2 à +2 vers hauteur du graphique)
            normalized_error = max(-2, min(2, error))
            y = self.rect.centery - (normalized_error / 2) * (self.rect.height // 2 - 10)
            points.append((x, y))
        
        if len(points) > 1:
            pygame.draw.lines(surface, color, False, points, 2)

class Simulator:
    """Simulateur principal"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Simulateur Moose Test PID - Robot suiveur de ligne")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)
        
        # Piste
        self.track = MooseTestTrack(TRACK_WIDTH, SCREEN_HEIGHT)
        self.track_surface = self.track.generate_track()
        
        # Robots
        start_x, start_y = 50, SCREEN_HEIGHT // 2
        self.robot1 = Robot(start_x, start_y - 30, BLUE, "Robot 1")
        self.robot2 = Robot(start_x, start_y + 30, ORANGE, "Robot 2")
        
        # Interface
        self.error_graph = ErrorGraph(TRACK_WIDTH + 10, 50, INFO_PANEL_WIDTH - 20, 200)
        
        # État
        self.running = True
        self.recording = False
        self.recorded_frames = []
        
        # Touches
        self.keys_pressed = set()
    
    def handle_events(self):
        """Gestion des événements"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                self.keys_pressed.add(event.key)
                
                # Commandes spéciales
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r:
                    self.reset_simulation()
                elif event.key == pygame.K_F1:
                    self.save_screenshot()
                elif event.key == pygame.K_F2:
                    self.toggle_recording()
            
            elif event.type == pygame.KEYUP:
                if event.key in self.keys_pressed:
                    self.keys_pressed.remove(event.key)
        
        # Réglage PID continu
        self.handle_pid_adjustments()
    
    def handle_pid_adjustments(self):
        """Gestion des réglages PID en temps réel"""
        adjust_speed = 0.01
        
        # Robot 1
        if pygame.K_q in self.keys_pressed:
            self.robot1.pid.kp += adjust_speed
        if pygame.K_a in self.keys_pressed:
            self.robot1.pid.kp = max(0, self.robot1.pid.kp - adjust_speed)
        if pygame.K_w in self.keys_pressed:
            self.robot1.pid.ki += adjust_speed * 0.1
        if pygame.K_s in self.keys_pressed:
            self.robot1.pid.ki = max(0, self.robot1.pid.ki - adjust_speed * 0.1)
        if pygame.K_e in self.keys_pressed:
            self.robot1.pid.kd += adjust_speed
        if pygame.K_d in self.keys_pressed:
            self.robot1.pid.kd = max(0, self.robot1.pid.kd - adjust_speed)
        
        # Robot 2
        if pygame.K_u in self.keys_pressed:
            self.robot2.pid.kp += adjust_speed
        if pygame.K_j in self.keys_pressed:
            self.robot2.pid.kp = max(0, self.robot2.pid.kp - adjust_speed)
        if pygame.K_i in self.keys_pressed:
            self.robot2.pid.ki += adjust_speed * 0.1
        if pygame.K_k in self.keys_pressed:
            self.robot2.pid.ki = max(0, self.robot2.pid.ki - adjust_speed * 0.1)
        if pygame.K_o in self.keys_pressed:
            self.robot2.pid.kd += adjust_speed
        if pygame.K_l in self.keys_pressed:
            self.robot2.pid.kd = max(0, self.robot2.pid.kd - adjust_speed)
    
    def reset_simulation(self):
        """Remet à zéro la simulation"""
        start_x, start_y = 50, SCREEN_HEIGHT // 2
        self.robot1.reset_position(start_x, start_y - 30)
        self.robot2.reset_position(start_x, start_y + 30)
    
    def save_screenshot(self):
        """Sauvegarde une capture d'écran"""
        timestamp = int(time.time())
        filename = f"moose_test_screenshot_{timestamp}.png"
        pygame.image.save(self.screen, filename)
        print(f"Capture sauvegardée: {filename}")
    
    def toggle_recording(self):
        """Démarre/arrête l'enregistrement"""
        if not self.recording:
            self.recording = True
            self.recorded_frames = []
            print("Enregistrement démarré...")
        else:
            self.recording = False
            self.save_recording()
    
    def save_recording(self):
        """Sauvegarde l'enregistrement (nécessite imageio - simulation seulement)"""
        if self.recorded_frames:
            print(f"Enregistrement terminé: {len(self.recorded_frames)} frames")
            # Note: imageio n'est pas disponible, simulation de la sauvegarde
            print("Note: Pour sauvegarder en GIF, installez imageio avec: pip install imageio")
    
    def draw_info_panel(self):
        """Dessine le panneau d'informations"""
        panel_x = TRACK_WIDTH
        y_offset = 270
        
        # Fond du panneau
        pygame.draw.rect(self.screen, DARK_GRAY, (panel_x, 0, INFO_PANEL_WIDTH, SCREEN_HEIGHT))
        pygame.draw.line(self.screen, WHITE, (panel_x, 0), (panel_x, SCREEN_HEIGHT), 2)
        
        # Informations Robot 1
        y_offset = self.draw_robot_info(self.robot1, panel_x + 10, y_offset)
        y_offset += 20
        
        # Informations Robot 2
        y_offset = self.draw_robot_info(self.robot2, panel_x + 10, y_offset)
        y_offset += 30
        
        # Commandes
        self.draw_controls(panel_x + 10, y_offset)
    
    def draw_robot_info(self, robot: Robot, x: int, y: int) -> int:
        """Dessine les informations d'un robot"""
        # Nom du robot
        name_text = self.font.render(robot.name, True, robot.color)
        self.screen.blit(name_text, (x, y))
        y += 25
        
        # Valeurs PID
        pid_info = [
            f"Kp: {robot.pid.kp:.3f}",
            f"Ki: {robot.pid.ki:.3f}",
            f"Kd: {robot.pid.kd:.3f}",
            f"Erreur: {robot.current_error:.3f}",
            f"Sortie: {robot.pid_output:.3f}"
        ]
        
        for info in pid_info:
            text = self.small_font.render(info, True, WHITE)
            self.screen.blit(text, (x, y))
            y += 18
        
        return y
    
    def draw_controls(self, x: int, y: int):
        """Dessine l'aide des commandes"""
        title = self.font.render("Commandes:", True, WHITE)
        self.screen.blit(title, (x, y))
        y += 25
        
        controls = [
            "Robot 1 (Bleu):",
            "Q/A: Kp  W/S: Ki  E/D: Kd",
            "",
            "Robot 2 (Orange):",
            "U/J: Kp  I/K: Ki  O/L: Kd",
            "",
            "R: Reset",
            "F1: Screenshot",
            "F2: Record",
            "ESC: Quitter"
        ]
        
        for control in controls:
            color = BLUE if "Robot 1" in control else ORANGE if "Robot 2" in control else WHITE
            text = self.small_font.render(control, True, color)
            self.screen.blit(text, (x, y))
            y += 16
    
    def update(self):
        """Met à jour la simulation"""
        self.robot1.update(self.track_surface)
        self.robot2.update(self.track_surface)
    
    def draw(self):
        """Dessine la simulation"""
        # Piste
        self.screen.blit(self.track_surface, (0, 0))
        
        # Robots
        self.robot1.draw(self.screen)
        self.robot2.draw(self.screen)
        
        # Panneau d'informations
        self.draw_info_panel()
        
        # Graphique d'erreur
        self.error_graph.draw(self.screen, self.robot1, self.robot2)
        
        # Enregistrement
        if self.recording:
            # Convertit la surface en array pour l'enregistrement
            frame_array = pygame.surfarray.array3d(self.screen)
            self.recorded_frames.append(frame_array)
            
            # Indicateur d'enregistrement
            pygame.draw.circle(self.screen, RED, (SCREEN_WIDTH - 30, 30), 10)
    
    def run(self):
        """Boucle principale"""
        print("Simulateur Moose Test PID démarré!")
        print("Utilisez les touches Q/A, W/S, E/D pour ajuster le PID du robot bleu")
        print("Utilisez les touches U/J, I/K, O/L pour ajuster le PID du robot orange")
        
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        print("Simulation terminée!")

def main():
    """Fonction principale"""
    try:
        simulator = Simulator()
        simulator.run()
    except Exception as e:
        print(f"Erreur: {e}")
        pygame.quit()

if __name__ == "__main__":
    main()