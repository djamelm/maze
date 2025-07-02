import pygame
import sys

# Initialisation
pygame.init()
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moose Test Simulation - PID Replay")
clock = pygame.time.Clock()

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Paramètres PID initiaux
Kp = 0.4  #1.25
Ki = 0.00001
Kd = 2.0  #0.3

def line_path(x):
    if x < 200:
        return HEIGHT // 2
    elif x < 300:
        return HEIGHT // 2 - 60
    elif x < 400:
        return HEIGHT // 2 + 60
    else:
        return HEIGHT // 2

def run_simulation():
    global Kp, Ki, Kd

    # Initialisation robot
    robot_x = 50
    robot_y = HEIGHT // 2
    error_sum = 0
    last_error = 0
    robot_radius = 10

    running = True
    while running:
        screen.fill(BLACK)

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q: Kp += 0.05
                elif event.key == pygame.K_a: Kp = max(0, Kp - 0.05)
                elif event.key == pygame.K_w: Ki += 0.00001
                elif event.key == pygame.K_s: Ki = max(0, Ki - 0.00001)
                elif event.key == pygame.K_e: Kd += 0.1
                elif event.key == pygame.K_d: Kd = max(0, Kd - 0.1)
                elif event.key == pygame.K_r: Kp, Ki, Kd = 0.4, 0.00001, 2.0
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Affichage de la ligne noire
        for x in range(WIDTH):
            y = line_path(x)
            pygame.draw.circle(screen, WHITE, (x, int(y)), 1)

        # PID
        target_y = line_path(robot_x)
        error = target_y - robot_y
        error_sum += error
        error_sum = max(min(error_sum, 10000), -10000)
        d_error = error - last_error
        last_error = error

        correction = Kp * error + Ki * error_sum + Kd * d_error
        correction = max(min(correction, 3), -3)


        robot_y += correction
        robot_y = max(0, min(robot_y, HEIGHT))
        robot_x += 0.8

        # Robot
        pygame.draw.circle(screen, RED, (int(robot_x), int(robot_y)), robot_radius)

        # Affichage texte
        font = pygame.font.SysFont(None, 24)
        screen.blit(font.render(f"Err={int(error)}  P={int(Kp*error)}  D={int(Kd*d_error)}", True, (255, 255, 255)), (10, 10))
        screen.blit(font.render(f"Kp={Kp:.2f} Ki={Ki:.5f} Kd={Kd:.2f}", True, (255, 255, 255)), (10, 30))
        screen.blit(font.render(f"[Q/A] Kp  [W/S] Ki  [E/D] Kd  [R] Reset  [ESC] Quit", True, (255, 255, 255)), (10, 50))

        pygame.display.flip()
        clock.tick(60)

        if robot_x > WIDTH:
            return  # Fin du run → relance dans boucle externe

# 💫 Boucle principale avec REPLAY
while True:
    run_simulation()
