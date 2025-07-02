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

# Initialisation Pygame
pygame.init()
WIDTH, HEIGHT = 1200, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulateur Moose Test PID")
CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont("consolas", 18)


# Paramètres PID initiaux
Kp = 0.4  #1.25
Ki = 0.00001
Kd = 2.0  #0.3