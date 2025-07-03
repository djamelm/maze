import pygame
import math
import random
from src.pid_controller import *
from configuration.colors import *
from configuration.screen import *

class Track:
    """Générateur de piste Moose Test"""
    def __init__(self, width: int = TRACK_WIDTH, height: int = SCREEN_HEIGHT):
        self.width = width
        self.height = height
        self.line_width = LINE_WIDTH
        self.set_track_points_init()
        
    def set_track_points(self, points=[(0, SCREEN_HEIGHT // 2),(TRACK_WIDTH, SCREEN_HEIGHT // 2),]):
        self.points = points
    def set_track_points_init(self):
        self.points = [
            # Phase 1: ligne droite
            (50, self.height // 2),
            (150, self.height // 2),
            # Phase 2: évitement rapide (S-curve)
            (250, self.height // 2 - 50),
            (350, self.height // 2 - 50),
             # Phase 3: retour au centre avec oscillations
            (450, self.height // 2),
            (550, self.height // 2 + 50),
            (650, self.height // 2 + 50),
            # Phase 4: ligne droite finale
            (750, self.height // 2),
            (950, self.height // 2)
        ]
    def get_track_points(self):
        return self.points
    def draw_track(self,screen):
        """Génère la piste de Moose Test"""
        # Ligne blanche avec trajectoire Moose Test
        points = self.points
        # Fond de piste
        # pygame.draw.rect(surface, LINE_COLOR, (0, 0, TRACK_WIDTH, SCREEN_HEIGHT))
        # Dessine la ligne épaisse
        if len(points) > 1:
            for i in range(len(points) - 1):
                pygame.draw.line(screen, LINE_COLOR, points[i], points[i + 1], self.line_width)
        return screen
    
    def draw_track(self, screen: pygame.Surface):
        points = self.points
        if len(points) > 1:
            for i in range(len(points) - 1):
                pygame.draw.line(screen, LINE_COLOR, points[i], points[i + 1], self.line_width)