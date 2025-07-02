import pygame
import math
import random

# --- Initialisation Pygame ---
pygame.init()
WIDTH, HEIGHT = 1200, 700
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulateur PID avec courbe d'erreur intégrée")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 16)

# --- Constantes ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
BLUE = (50, 150, 255)
ORANGE = (255, 150, 50)
LIGHT_GREEN = (0, 255, 120)
DARK_RED = (180, 0, 0)

ROBOT_LENGTH = 40
ROBOT_WIDTH = 30
IR_COUNT = 5
IR_WEIGHTS = [-2, -1, 0, 1, 2]
IR_SPACING = 12
IR_SIZE = 5

GRAPH_WIDTH = 300
MAX_ERROR_HISTORY = GRAPH_WIDTH

# --- Trajectoire continue ---
def line_path(x):
    return HEIGHT // 2 + 80 * math.sin(0.005 * x) + 30 * math.sin(0.03 * x)

def draw_path(surface, noise=10):
    pygame.draw.rect(surface, BLACK, (0, 0, WIDTH, HEIGHT))
    for x in range(WIDTH - GRAPH_WIDTH):
        y = line_path(x)
        pygame.draw.circle(surface, WHITE, (x, int(y)), 1)
    for _ in range(noise):
        x = random.randint(100, WIDTH - GRAPH_WIDTH - 100)
        w = random.randint(10, 30)
        pygame.draw.rect(surface, GREY, (x, 0, w, HEIGHT))

def get_ir_positions(x, y, angle):
    cos_a, sin_a = math.cos(angle), math.sin(angle)
    return [(x + (ROBOT_LENGTH / 2) * cos_a - (i - IR_COUNT // 2) * IR_SPACING * sin_a,
             y + (ROBOT_LENGTH / 2) * sin_a + (i - IR_COUNT // 2) * IR_SPACING * cos_a)
            for i in range(IR_COUNT)]

def read_ir(path_surface, positions):
    readings = []
    for (x, y) in positions:
        if 0 <= int(x) < WIDTH and 0 <= int(y) < HEIGHT:
            color = path_surface.get_at((int(x), int(y)))[:3]
        else:
            color = (0, 0, 0)
        readings.append(1 if color == WHITE else 0)
    return readings

def pid_create(kp, ki, kd):
    return {"Kp": kp, "Ki": ki, "Kd": kd, "sum": 0, "last": 0}

def pid_compute(pid, error):
    pid["sum"] += error
    d = error - pid["last"]
    pid["last"] = error
    P = pid["Kp"] * error
    I = pid["Ki"] * pid["sum"]
    D = pid["Kd"] * d
    return P + I + D, P, I, D

def draw_robot(x, y, a, ir_vals, color):
    cos_a, sin_a = math.cos(a), math.sin(a)
    half_L, half_W = ROBOT_LENGTH / 2, ROBOT_WIDTH / 2
    corners = [(x + dx * cos_a - dy * sin_a, y + dx * sin_a + dy * cos_a)
               for dx, dy in [(-half_L, -half_W), (-half_L, half_W), (half_L, half_W), (half_L, -half_W)]]
    pygame.draw.polygon(screen, color, corners, 2)
    ir_pos = get_ir_positions(x, y, a)
    for i, (ix, iy) in enumerate(ir_pos):
        c = LIGHT_GREEN if ir_vals[i] else DARK_RED
        pygame.draw.circle(screen, c, (int(ix), int(iy)), IR_SIZE)

def draw_error_graph(data1, data2):
    graph_x = WIDTH - GRAPH_WIDTH
    pygame.draw.rect(screen, (30, 30, 30), (graph_x, 0, GRAPH_WIDTH, HEIGHT))
    if len(data1) > 1:
        for i in range(1, len(data1)):
            pygame.draw.line(screen, BLUE,
                             (graph_x + i - 1, HEIGHT//2 - data1[i-1]*20),
                             (graph_x + i, HEIGHT//2 - data1[i]*20), 2)
    if len(data2) > 1:
        for i in range(1, len(data2)):
            pygame.draw.line(screen, ORANGE,
                             (graph_x + i - 1, HEIGHT//2 - data2[i-1]*20),
                             (graph_x + i, HEIGHT//2 - data2[i]*20), 2)

def reset_robot(color, offset=0):
    return {"x": 100, "y": line_path(100) + offset, "a": 0,
            "pid": pid_create(0.6, 0.0, 0.2), "c": color, "traj": []}

# --- Initialisation ---
draw_path(screen)
path_surface = screen.copy()
robot1 = reset_robot(BLUE, 0)
robot2 = reset_robot(ORANGE, 20)
plot_data1 = []
plot_data2 = []

running = True
while running:
    clock.tick(FPS)
    screen.blit(path_surface, (0, 0))

    for robot, plot in zip([robot1, robot2], [plot_data1, plot_data2]):
        ir_pos = get_ir_positions(robot["x"], robot["y"], robot["a"])
        ir_vals = read_ir(path_surface, ir_pos)
        active = sum(ir_vals)
        err = sum(IR_WEIGHTS[i] * ir_vals[i] for i in range(IR_COUNT))
        error = err / active if active else 0
        correction, *_ = pid_compute(robot["pid"], error)
        robot["a"] += correction * 0.02
        robot["x"] += 2 * math.cos(robot["a"])
        robot["y"] += 2 * math.sin(robot["a"])
        robot["traj"].append((robot["x"], robot["y"]))
        for i in range(1, len(robot["traj"])):
            pygame.draw.line(screen, robot["c"], robot["traj"][i - 1], robot["traj"][i], 1)
        draw_robot(robot["x"], robot["y"], robot["a"], ir_vals, robot["c"])
        plot.append(error)
        if len(plot) > MAX_ERROR_HISTORY:
            plot.pop(0)

    draw_error_graph(plot_data1, plot_data2)
    pygame.display.flip()

    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
            running = False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_r:
                robot1 = reset_robot(BLUE, 0)
                robot2 = reset_robot(ORANGE, 20)
                plot_data1.clear()
                plot_data2.clear()
            # Contrôle robot 1
            elif e.key == pygame.K_q: robot1["pid"]["Kp"] += 0.1
            elif e.key == pygame.K_a: robot1["pid"]["Kp"] = max(0, robot1["pid"]["Kp"] - 0.1)
            elif e.key == pygame.K_w: robot1["pid"]["Ki"] += 0.01
            elif e.key == pygame.K_s: robot1["pid"]["Ki"] = max(0, robot1["pid"]["Ki"] - 0.01)
            elif e.key == pygame.K_e: robot1["pid"]["Kd"] += 0.05
            elif e.key == pygame.K_d: robot1["pid"]["Kd"] = max(0, robot1["pid"]["Kd"] - 0.05)
            # Contrôle robot 2
            elif e.key == pygame.K_u: robot2["pid"]["Kp"] += 0.1
            elif e.key == pygame.K_j: robot2["pid"]["Kp"] = max(0, robot2["pid"]["Kp"] - 0.1)
            elif e.key == pygame.K_i: robot2["pid"]["Ki"] += 0.01
            elif e.key == pygame.K_k: robot2["pid"]["Ki"] = max(0, robot2["pid"]["Ki"] - 0.01)
            elif e.key == pygame.K_o: robot2["pid"]["Kd"] += 0.05
            elif e.key == pygame.K_l: robot2["pid"]["Kd"] = max(0, robot2["pid"]["Kd"] - 0.05)

pygame.quit()
