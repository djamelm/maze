import pygame
import math
import sys
import os
from datetime import datetime

# Configuration
WIDTH, HEIGHT = 1000, 700
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND_COLOR = BLACK
LINE_COLOR = WHITE
SENSOR_THRESHOLD = 5
MAX_HISTORY = 200

# Initialisation Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulateur Moose Test PID")
clock = pygame.time.Clock()

# Fonction de tracé de ligne (Moose Test)
def line_path(x):
    """Ligne blanche avec virage en S pour le Moose Test"""
    if x < 300:
        return 400
    elif x < 600:
        return 400 + 150 * math.sin((x-300)*math.pi/150)
    else:
        return 400 + 150 * math.sin((x-600)*math.pi/150)

class Robot:
    def __init__(self, x, y, color, pid_values):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 2
        self.color = color
        self.Kp, self.Ki, self.Kd = pid_values
        self.error_sum = 0
        self.last_error = 0
        self.width = 40
        self.height = 20
        self.trail = []
        self.error_history = []
        self.weights = [-2, -1, 0, 1, 2]
        self.start_pos = (x, y)
        self.sensor_positions = []
        self.calculate_sensor_positions()
        
    def calculate_sensor_positions(self):
        """Calcul des positions des capteurs avec rotation"""
        self.sensor_positions = []
        spacing = 10
        front_y = -self.height/2 - 5  # 5 pixels devant le robot
        
        for i in range(5):
            local_x = -20 + i * spacing
            angle_rad = math.radians(self.angle)
            rotated_x = local_x * math.cos(angle_rad) - front_y * math.sin(angle_rad)
            rotated_y = local_x * math.sin(angle_rad) + front_y * math.cos(angle_rad)
            self.sensor_positions.append((
                self.x + rotated_x,
                self.y + rotated_y
            ))
    
    def get_sensor_values(self):
        """Lecture des capteurs IR simulés"""
        values = []
        for sx, sy in self.sensor_positions:
            line_y = line_path(sx)
            if abs(sy - line_y) <= SENSOR_THRESHOLD:
                values.append(0)  # Sur la ligne (blanche)
            else:
                values.append(1024)  # Hors ligne (noir)
        return values
    
    def update_pid(self):
        """Calcul du contrôle PID"""
        values = self.get_sensor_values()
        error = sum(w * v for w, v in zip(self.weights, values))
        
        self.error_sum += error
        derivative = error - self.last_error
        output = self.Kp * error + self.Ki * self.error_sum + self.Kd * derivative
        self.last_error = error
        
        # Mise à jour de l'angle
        self.angle += output * 0.01
        
        # Mémorisation pour visualisation
        self.error_history.append(error)
        if len(self.error_history) > MAX_HISTORY:
            self.error_history.pop(0)
        
        return error
    
    def update_position(self):
        """Mise à jour de la position du robot"""
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y += self.speed * math.sin(math.radians(self.angle))
        self.calculate_sensor_positions()
        self.trail.append((self.x, self.y))
        if len(self.trail) > 500:
            self.trail.pop(0)
    
    def reset(self):
        """Réinitialisation du robot"""
        self.x, self.y = self.start_pos
        self.angle = 0
        self.error_sum = 0
        self.last_error = 0
        self.trail = []
        self.error_history = []
    
    def draw(self, surface):
        """Affichage du robot et de ses capteurs"""
        # Surface du robot
        robot_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        robot_surf.fill((*self.color, 180))
        pygame.draw.rect(robot_surf, (0, 0, 0), (0, 0, self.width, self.height), 2)
        
        # Rotation et affichage
        rotated_surf = pygame.transform.rotate(robot_surf, -self.angle)
        rect = rotated_surf.get_rect(center=(self.x, self.y))
        surface.blit(rotated_surf, rect.topleft)
        
        # Capteurs
        for sx, sy in self.sensor_positions:
            pygame.draw.circle(surface, (255, 255, 0), (int(sx), int(sy)), 3)
        
        # Chemin parcouru
        if len(self.trail) > 1:
            pygame.draw.lines(surface, self.color, False, self.trail, 2)

def draw_line(surface):
    """Dessine la trajectoire blanche"""
    points = []
    for x in range(0, WIDTH+1, 5):
        points.append((x, line_path(x)))
    if len(points) > 1:
        pygame.draw.lines(surface, LINE_COLOR, False, points, 8)

def draw_ui(surface, robot1, robot2):
    """Interface utilisateur"""
    font = pygame.font.SysFont(None, 20)
    
    # Informations PID
    info1 = f"R1: Kp={robot1.Kp:.2f} Ki={robot1.Ki:.2f} Kd={robot1.Kd:.2f} | Err={robot1.last_error:.0f}"
    info2 = f"R2: Kp={robot2.Kp:.2f} Ki={robot2.Ki:.2f} Kd={robot2.Kd:.2f} | Err={robot2.last_error:.0f}"
    text1 = font.render(info1, True, robot1.color)
    text2 = font.render(info2, True, robot2.color)
    surface.blit(text1, (WIDTH-400, 10))
    surface.blit(text2, (WIDTH-400, 30))
    
    # Commandes
    keys = "Q/A: Kp1 | W/S: Ki1 | E/D: Kd1 | U/J: Kp2 | I/K: Ki2 | O/L: Kd2 | R: Réinitialiser | ESC: Quitter"
    key_text = font.render(keys, True, WHITE)
    surface.blit(key_text, (10, 10))
    
    # Flèche de direction
    arrow_points = [(0, 0), (-10, -5), (-5, 0), (-10, 5)]
    max_err = 1000
    scale = min(abs(robot1.last_error)/max_err, 1) * 20
    arrow_surf = pygame.Surface((40, 40), pygame.SRCALPHA)
    arrow = [(x*scale + 20, y*scale + 20) for x, y in arrow_points]
    pygame.draw.polygon(arrow_surf, robot1.color, arrow)
    rotated_arrow = pygame.transform.rotate(arrow_surf, -robot1.angle)
    rect = rotated_arrow.get_rect(center=(WIDTH-100, HEIGHT-50))
    surface.blit(rotated_arrow, rect.topleft)

def draw_error_curve(surface, robot, x_offset, color):
    """Courbe d'erreur en temps réel"""
    curve_rect = pygame.Rect(WIDTH-200+x_offset, 100, 180, 600)
    points = []
    for i, err in enumerate(robot.error_history):
        x = curve_rect.x + i
        y = curve_rect.centery - err/5  # Échelle adaptée
        points.append((x, y))
    
    pygame.draw.rect(surface, (40, 40, 40), curve_rect)
    if len(points) > 1:
        pygame.draw.lines(surface, color, False, points, 2)

def save_screenshot():
    """Enregistre une capture d'écran"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    pygame.image.save(screen, filename)
    print(f"Capture sauvegardée : {filename}")

def main():
    # Initialisation des robots
    robot1 = Robot(100, 400, (255, 0, 0), [1.2, 0.01, 0.1])
    robot2 = Robot(100, 400, (0, 255, 0), [1.0, 0.0, 0.05])
    
    running = True
    recording = False
    frames = []
    
    while running:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Contrôles clavier
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    robot1.reset()
                    robot2.reset()
                elif event.key == pygame.K_F1:
                    save_screenshot()
                elif event.key == pygame.K_q:
                    robot1.Kp += 0.05
                elif event.key == pygame.K_a:
                    robot1.Kp -= 0.05
                elif event.key == pygame.K_w:
                    robot1.Ki += 0.001
                elif event.key == pygame.K_s:
                    robot1.Ki -= 0.001
                elif event.key == pygame.K_e:
                    robot1.Kd += 0.01
                elif event.key == pygame.K_d:
                    robot1.Kd -= 0.01
                elif event.key == pygame.K_u:
                    robot2.Kp += 0.05
                elif event.key == pygame.K_j:
                    robot2.Kp -= 0.05
                elif event.key == pygame.K_i:
                    robot2.Ki += 0.001
                elif event.key == pygame.K_k:
                    robot2.Ki -= 0.001
                elif event.key == pygame.K_o:
                    robot2.Kd += 0.01
                elif event.key == pygame.K_l:
                    robot2.Kd -= 0.01
        
        # Mise à jour
        robot1.update_position()
        robot1.update_pid()
        robot2.update_position()
        robot2.update_pid()
        
        # Dessin
        screen.fill(BACKGROUND_COLOR)
        draw_line(screen)
        robot1.draw(screen)
        robot2.draw(screen)
        draw_ui(screen, robot1, robot2)
        draw_error_curve(screen, robot1, 0, robot1.color)
        draw_error_curve(screen, robot2, 190, robot2.color)
        
        # Enregistrement GIF
        if recording:
            frame = pygame.surfarray.array3d(screen)
            frame = frame.swapaxes(0, 1)
            frames.append(frame)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()