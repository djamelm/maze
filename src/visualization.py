import pygame
from typing import List, Tuple
from configuration.colors import *
from configuration.screen import *

class Visualization:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont('Arial', 18)
        self.title_font = pygame.font.SysFont('Arial', 28, bold=True)

    def draw_info(self, surface, robots, selected):
        """Affiche les informations PID des robots."""
        y = 10
        for i, r in enumerate(robots):
            name = f"Robot {i+1} (Kp={r.pid.kp:.2f}, Ki={r.pid.ki:.2f}, Kd={r.pid.kd:.2f})"
            text = self.font.render(name, True, BLUE if i == 0 else ORANGE)
            surface.blit(text, (10, y))
            y += 25

        controls = [
            "Contrôles Robot 1: Q/A Kp, W/S Ki, E/D Kd",
            "Contrôles Robot 2: U/J Kp, I/K Ki, O/L Kd",
            "R: Reset | F1: Screenshot | ESC: Quit"
        ]
        for line in controls:
            text = self.font.render(line, True, WHITE)
            surface.blit(text, (10, y))
            y += 22

    def draw_pid_graph(self, surface, errors1, errors2, x, y, width, height):
        """Dessine le graphique PID"""
        # Cadre du graphique
        pygame.draw.rect(surface, (40, 40, 60), (x, y, width, height))
        pygame.draw.rect(surface, (100, 100, 150), (x, y, width, height), 2)
        
        # Titre
        title = self.title_font.render("Erreur PID", True, LIGHT_BLUE)
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
                px = x + width - (len(errors1) - i) * width/100
                py = y + min(height, max(-height,height//2 - error * height//3))
                points.append((px, py))
            
            pygame.draw.lines(surface, BLUE, False, points, 2)
        
        # Courbe d'erreur pour le robot 2
        if len(errors2) > 1:
            points = []
            for i, error in enumerate(errors2):
                px = x + width - (len(errors2) - i) *  width/100
                py = y + min(height, max(-height,height//2 - error * height//3))
                points.append((px, py))
            
            pygame.draw.lines(surface, ORANGE, False, points, 2)
        
        # Légendes
        pygame.draw.line(surface, BLUE, (x + 20, y + height - 30), (x + 50, y + height - 30), 2)
        pygame.draw.line(surface, ORANGE, (x + 20, y + height - 10), (x + 50, y + height - 10), 2)
        
        text1 = self.font.render("Robot 1", True, BLUE)
        text2 = self.font.render("Robot 2", True, ORANGE)
        surface.blit(text1, (x + 60, y + height - 45))
        surface.blit(text2, (x + 60, y + height - 25))

    def draw_title(self, surface):
        """Dessine le titre principal de la simulation."""
        title = self.title_font.render("Simulation Moose Test - Robot Suiveur de Ligne PID", True, YELLOW)
        surface.blit(title, (self.width // 2 - title.get_width() // 2, 10))

        info_text = self.font.render("Utilisez les touches pour ajuster les paramètres PID en temps réel", True, LIGHT_BLUE)
        surface.blit(info_text, (self.width // 2 - info_text.get_width() // 2, self.height - 30))
