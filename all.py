#!/usr/bin/env python3
"""
Simulateur Moose Test PID - Robot suiveur de ligne
Simulation réaliste avec contrôle PID, visualisation temps réel et comparaison de deux robots
"""
# Importation des bibliothèques nécessaires
import pygame
import math
import random
from datetime import datetime
import sys
from pygame import gfxdraw
import imageio
import os
import asyncio
import platform
import time
from configuration.robot import *
from configuration.colors import *
from src.robot import *
from src.track import *
from src.utils import save_screenshot, handle_events, record_frame

# Initialisation Pygame
pygame.init()
WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(BACKGROUND)
pygame.display.set_caption("Simulateur Moose Test PID")
clock = pygame.time.Clock()
# Police
font = pygame.font.SysFont('Arial', 18)
title_font = pygame.font.SysFont('Arial', 28, bold=True)

track = Track()

# Paramètres PID initiaux
Kp = 0.4  #1.25
Ki = 0.00001
Kd = 2.0  #0.3


# Initialisation robots
robots = [
    Robot(50, HEIGHT // 2+5, BLUE, 0.1, 0.1, 0.1, 'djamel', 90),
    Robot(50, HEIGHT // 2-10, ORANGE, 0.2, 0.0, 0.1, 'ahmed', 90),
]
# Boucle principale
running = True
# Variables pour l'enregistrement
recording = False
frames = []

while running:
    # Gestion des événements
    running, recording, frames = handle_events(robots, screen, running, recording, frames)

    # Effacer l'écran
    screen.fill(BACKGROUND)
    track.draw_track(screen)
    draw_info(screen, robots, 0)

    # Logique de mise à jour des robots et Dessiner les éléments de la simulation
    for robot in robots:
        robot.draw(screen)
        robot.update(track)
        draw_pid_graph(screen, robots[0].pid.error_history, robots[1].pid.error_history, TRACK_WIDTH, 0, GRAPH_WIDTH, HEIGHT // 2)

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Enregistrer le cadre actuel si en mode enregistrement
    frames = record_frame(screen, recording, frames)

    # Limiter le taux de rafraîchissement
    clock.tick(60)
    pygame.display.flip()