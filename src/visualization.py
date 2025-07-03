
from configuration.robot import *
from configuration.colors import *
from src.robot import *
from src.track import *
# Police
font = pygame.font.SysFont('Arial', 18)
title_font = pygame.font.SysFont('Arial', 28, bold=True)
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
            
# Draw HUD
def draw_hud(surface, robot1, robot2):
    font = pygame.font.SysFont('arial', 20)
    texts = [
        f"Robot 1 (Blue) - Error: {robot1.error:.2f}",
        f"Kp: {robot1.kp:.3f} (Q/A)",
        f"Ki: {robot1.ki:.3f} (W/S)",
        f"Kd: {robot1.kd:.3f} (E/D)",
        f"Robot 2 (Orange) - Error: {robot2.error:.2f}",
        f"Kp: {robot2.kp:.3f} (U/J)",
        f"Ki: {robot2.ki:.3f} (I/K)",
        f"Kd: {robot2.kd:.3f} (O/L)",
        "R: Reset, F1: Screenshot, F2: Toggle GIF, ESC: Quit"
    ]
    for i, text in enumerate(texts):
        surface.blit(font.render(text, True, WHITE), (TRACK_WIDTH + 10, 10 + i * 30))
        
# Draw PID graph
def draw_pid_graph(surface, robot1, robot2):
    graph_surface = pygame.Surface((GRAPH_WIDTH, HEIGHT))
    graph_surface.fill((50, 50, 50))
    
    # Draw grid
    for y in range(0, HEIGHT, 50):
        pygame.draw.line(graph_surface, (100, 100, 100), (0, y), (GRAPH_WIDTH, y))
    pygame.draw.line(graph_surface, (150, 150, 150), (0, HEIGHT // 2), (GRAPH_WIDTH, HEIGHT // 2), 2)

    # Draw error curves
    for i, error in enumerate(robot1.error_history):
        y = HEIGHT // 2 - int(error * 0.1)
        y = max(0, min(HEIGHT - 1, y))
        pygame.draw.circle(graph_surface, BLUE, (i, y), 1)
    for i, error in enumerate(robot2.error_history):
        y = HEIGHT // 2 - int(error * 0.1)
        y = max(0, min(HEIGHT - 1, y))
        pygame.draw.circle(graph_surface, ORANGE, (i, y), 1)

    surface.blit(graph_surface, (TRACK_WIDTH, 0))

    
        # Titre principal
        title = title_font.render("Simulation Moose Test - Robot Suiveur de Ligne PID", True, YELLOW)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 10))
        
        # Informations
        info_text = font.render("Utilisez les touches pour ajuster les paramètres PID en temps réel", True, LIGHT_BLUE)
        screen.blit(info_text, (WIDTH // 2 - info_text.get_width() // 2, HEIGHT - 30))