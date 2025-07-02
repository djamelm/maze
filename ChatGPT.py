# Importation des bibliothèques nécessaires
import pygame
import math
import random
from datetime import datetime

# Initialisation Pygame
pygame.init()
WIDTH, HEIGHT = 1200, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulateur Moose Test PID")
CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont("consolas", 18)

# Couleurs
BLACK, WHITE = (0, 0, 0), (255, 255, 255)
RED, BLUE, ORANGE, GREEN = (255, 0, 0), (0, 150, 255), (255, 140, 0), (0, 255, 0)
GREY = (30, 30, 30)

# Paramètres robot
ROBOT_WIDTH, ROBOT_HEIGHT = 40, 30
SENSOR_OFFSET = 20
SENSOR_DISTANCE = 10
LINE_WIDTH = 30

# Classe PID
class PID:
    def __init__(self, kp, ki, kd):
        self.kp, self.ki, self.kd = kp, ki, kd
        self.integral = 0
        self.last_error = 0

    def update(self, error):
        self.integral += error
        derivative = error - self.last_error
        self.last_error = error
        return self.kp * error + self.ki * self.integral + self.kd * derivative

# Classe Robot
class Robot:
    def __init__(self, x, y, color, pid):
        self.x, self.y = x, y
        self.angle = 0
        self.color = color
        self.pid = pid
        self.trail = []
        self.error_log = []
        self.reset()

    def reset(self):
        self.angle = 0
        self.pid.integral = 0
        self.pid.last_error = 0
        self.trail.clear()
        self.error_log.clear()
        self.x, self.y = 200, HEIGHT // 2

    def get_sensor_positions(self):
        sensors = []
        for i in range(-2, 3):
            dx = math.cos(math.radians(self.angle + i * 10)) * SENSOR_OFFSET
            dy = math.sin(math.radians(self.angle + i * 10)) * SENSOR_OFFSET
            sx = self.x + dx + i * SENSOR_DISTANCE
            sy = self.y + dy
            sensors.append((sx, sy))
        return sensors

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

    def update(self, surface):
        error = self.get_error(surface)
        correction = self.pid.update(error)
        self.angle += correction * 0.3
        self.x += math.cos(math.radians(self.angle)) * 2
        self.y += math.sin(math.radians(self.angle)) * 2
        self.trail.append((self.x, self.y))
        self.error_log.append(error)
        if len(self.error_log) > 300:
            self.error_log.pop(0)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 8)
        if len(self.trail) > 1:
            pygame.draw.lines(surface, self.color, False, self.trail, 2)
        # flèche PID
        dx = math.cos(math.radians(self.angle)) * 20
        dy = math.sin(math.radians(self.angle)) * 20
        pygame.draw.line(surface, GREEN, (self.x, self.y), (self.x + dx, self.y + dy), 2)
        # capteurs
        for sx, sy in self.get_sensor_positions():
            pygame.draw.circle(surface, WHITE, (int(sx), int(sy)), 2)

# Ligne à suivre (Moose Test)
def draw_line(surface):
    surface.fill(BLACK)
    for x in range(0, WIDTH, 1):
        y = int(HEIGHT//2 + 100 * math.sin(0.005 * x) * math.sin(0.05 * x))
        pygame.draw.circle(surface, WHITE, (x, y), LINE_WIDTH//2)

# Dessiner oscilloscope PID
def draw_pid_graph(surface, robots):
    graph_w = 300
    graph_h = HEIGHT
    graph_x = WIDTH - graph_w
    pygame.draw.rect(surface, GREY, (graph_x, 0, graph_w, graph_h))
    for i, robot in enumerate(robots):
        data = robot.error_log[-graph_w:]
        for x in range(1, len(data)):
            y1 = HEIGHT//2 - int(data[x-1] * 10)
            y2 = HEIGHT//2 - int(data[x] * 10)
            color = BLUE if i == 0 else ORANGE
            pygame.draw.line(surface, color, (graph_x + x - 1, y1), (graph_x + x, y2), 1)

# Afficher infos PID
def draw_info(surface, robots, selected):
    y = 10
    for i, r in enumerate(robots):
        name = f"Robot {i+1} (Kp={r.pid.kp:.2f}, Ki={r.pid.ki:.2f}, Kd={r.pid.kd:.2f})"
        text = FONT.render(name, True, BLUE if i == 0 else ORANGE)
        surface.blit(text, (10, y))
        y += 25
    controls = [
        "Contrôles Robot 1: Q/A Kp, W/S Ki, E/D Kd",
        "Contrôles Robot 2: U/J Kp, I/K Ki, O/L Kd",
        "R: Reset | F1: Screenshot | ESC: Quit"
    ]
    for line in controls:
        text = FONT.render(line, True, WHITE)
        surface.blit(text, (10, y))
        y += 22

# Capture
def save_screenshot():
    filename = f"screenshot_{datetime.now().strftime('%H%M%S')}.png"
    pygame.image.save(SCREEN, filename)

# Initialisation robots
robots = [
    Robot(200, HEIGHT // 2, BLUE, PID(0.5, 0.0, 0.2)),
    Robot(200, HEIGHT // 2, ORANGE, PID(0.3, 0.0, 0.1))
]

# Surface de la trajectoire
TRACK = pygame.Surface((WIDTH, HEIGHT))
draw_line(TRACK)

# Boucle principale
running = True
while running:
    CLOCK.tick(60)
    SCREEN.blit(TRACK, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_r:
                for robot in robots:
                    robot.reset()
            elif event.key == pygame.K_F1:
                save_screenshot()
            # Robot 1
            elif event.key == pygame.K_q:
                robots[0].pid.kp += 0.1
            elif event.key == pygame.K_a:
                robots[0].pid.kp -= 0.1
            elif event.key == pygame.K_w:
                robots[0].pid.ki += 0.01
            elif event.key == pygame.K_s:
                robots[0].pid.ki -= 0.01
            elif event.key == pygame.K_e:
                robots[0].pid.kd += 0.05
            elif event.key == pygame.K_d:
                robots[0].pid.kd -= 0.05
            # Robot 2
            elif event.key == pygame.K_u:
                robots[1].pid.kp += 0.1
            elif event.key == pygame.K_j:
                robots[1].pid.kp -= 0.1
            elif event.key == pygame.K_i:
                robots[1].pid.ki += 0.01
            elif event.key == pygame.K_k:
                robots[1].pid.ki -= 0.01
            elif event.key == pygame.K_o:
                robots[1].pid.kd += 0.05
            elif event.key == pygame.K_l:
                robots[1].pid.kd -= 0.05

    for robot in robots:
        robot.update(TRACK)
        robot.draw(SCREEN)

    draw_pid_graph(SCREEN, robots)
    draw_info(SCREEN, robots, 0)
    pygame.display.flip()

pygame.quit()
