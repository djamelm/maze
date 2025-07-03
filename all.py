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

# Initialisation Pygame
pygame.init()
WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(BACKGROUND)
pygame.display.set_caption("Simulateur Moose Test PID")
CLOCK = pygame.time.Clock()
# Police
font = pygame.font.SysFont('Arial', 18)
title_font = pygame.font.SysFont('Arial', 28, bold=True)

track = Track()

# Paramètres PID initiaux
Kp = 0.4  #1.25
Ki = 0.00001
Kd = 2.0  #0.3

# Afficher infos PID
def draw_info(surface, robots, selected):
    y = 10
    for i, r in enumerate(robots):
        name = f"Robot {i+1} (Kp={r.pid.kp:.2f}, Ki={r.pid.ki:.2f}, Kd={r.pid.kd:.2f})"
        text = font.render(name, True, BLUE if i == 0 else ORANGE)
        surface.blit(text, (10, y))
        y += 25
    controls = [
        "Contrôles Robot 1: Q/A Kp, W/S Ki, E/D Kd",
        "Contrôles Robot 2: U/J Kp, I/K Ki, O/L Kd",
        "R: Reset | F1: Screenshot | ESC: Quit"
    ]
    for line in controls:
        text = font.render(line, True, WHITE)
        surface.blit(text, (10, y))
        y += 22
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
            px = x + width - (len(errors1) - i) * 3
            py = y + height//2 - error * height//3
            points.append((px, py))
        
        pygame.draw.lines(surface, BLUE, False, points, 2)
    
    # Courbe d'erreur pour le robot 2
    if len(errors2) > 1:
        points = []
        for i, error in enumerate(errors2):
            px = x + width - (len(errors2) - i) * 3
            py = y + height//2 - error * height//3
            points.append((px, py))
        
        pygame.draw.lines(surface, ORANGE, False, points, 2)
    
    # Légendes
    pygame.draw.line(surface, BLUE, (x + 20, y + height - 30), (x + 50, y + height - 30), 2)
    pygame.draw.line(surface, ORANGE, (x + 20, y + height - 10), (x + 50, y + height - 10), 2)
    
    text1 = font.render("Robot 1", True, BLUE)
    text2 = font.render("Robot 2", True, ORANGE)
    surface.blit(text1, (x + 60, y + height - 45))
    surface.blit(text2, (x + 60, y + height - 25))

# Initialisation robots
robots = [
    Robot(50, HEIGHT // 2+5, BLUE, 0.1, 0.1, 0.1, 'djamel', 90),
    Robot(50, HEIGHT // 2-10, ORANGE, 0.2, 0.0, 0.1, 'ahmed', 90),
]
# Boucle principale
running = True
while running:
    CLOCK.tick(24)
    screen.fill(BACKGROUND)
    track.draw_track(screen)
    draw_info(screen, robots, 0)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Robot 1 PID controls
            if event.key == pygame.K_q:
                robots[0].pid.kp += 0.01
            elif event.key == pygame.K_a:
                robots[0].pid.kp = max(0, robots[0].pid.kp - 0.01)
            elif event.key == pygame.K_w:
                robots[0].pid.ki += 0.001
            elif event.key == pygame.K_s:
                robots[0].pid.ki = max(0, robots[0].pid.ki - 0.001)
            elif event.key == pygame.K_e:
                robots[0].pid.kd += 0.01
            elif event.key == pygame.K_d:
                robots[0].pid.kd = max(0, robots[0].pid.kd - 0.01)
            # Robot 2 PID controls
            elif event.key == pygame.K_u:
                robots[1].pid.kp += 0.01
            elif event.key == pygame.K_j:
                robots[1].pid.kp = max(0, robots[1].pid.kp - 0.01)
            elif event.key == pygame.K_i:
                robots[1].pid.ki += 0.001
            elif event.key == pygame.K_k:
                robots[1].pid.ki = max(0, robots[1].pid.ki - 0.001)
            elif event.key == pygame.K_o:
                robots[1].pid.kd += 0.01
            elif event.key == pygame.K_l:
                robots[1].pid.kd = max(0, robots[1].pid.kd - 0.01)
            # Other controls
            elif event.key == pygame.K_r:
                robots[0].reset()
                robots[1].reset()
            elif event.key == pygame.K_F1:
                pygame.image.save(screen, "screenshot.png")
            elif event.key == pygame.K_F2:
                recording = not recording
                if not recording and frames:
                    imageio.mimsave("simulation.gif", frames, fps=FPS)
                    frames = []
            elif event.key == pygame.K_ESCAPE:
                running = False
    for robot in robots:
        robot.draw(screen)
        draw_pid_graph(screen, robots[0].pid.error_history, robots[1].pid.error_history, TRACK_WIDTH, 0, GRAPH_WIDTH, HEIGHT // 2)
        robot.update(track)
    pygame.display.flip()