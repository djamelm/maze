import pygame
import imageio
import datetime

def save_screenshot(screen, prefix="screenshot"):
    """Enregistre une capture d'écran."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}.png"
    pygame.image.save(screen, filename)
    print(f"Capture sauvegardée : {filename}")

def handle_events(robots, screen, running, recording, frames):
    """Gère les événements du clavier et de la souris."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_r:
                # Reset des robots
                for robot in robots:
                    robot.reset()
            elif event.key == pygame.K_F1:
                # Capture d'écran
                save_screenshot(screen)
            elif event.key == pygame.K_F2:
                # Basculer l'enregistrement GIF
                recording = not recording
                if not recording and frames:
                    # Sauvegarder l'animation GIF
                    imageio.mimsave('simulation.gif', frames, fps=24)
                    frames = []

            # Commandes pour ajuster les paramètres PID du robot 1
            elif event.key == pygame.K_a:
                robots[0].pid.kp += 0.1
            elif event.key == pygame.K_q:
                robots[0].pid.kp -= 0.1
            elif event.key == pygame.K_z:
                robots[0].pid.ki += 0.01
            elif event.key == pygame.K_s:
                robots[0].pid.ki -= 0.01
            elif event.key == pygame.K_e:
                robots[0].pid.kd += 0.05
            elif event.key == pygame.K_d:
                robots[0].pid.kd -= 0.05

            # Commandes pour ajuster les paramètres PID du robot 2
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

    return running, recording, frames

def record_frame(screen, recording, frames):
    """Enregistre un cadre pour la création d'un GIF."""
    if recording:
        frame = pygame.surfarray.array3d(screen)
        frame = frame.swapaxes(0, 1)
        frames.append(frame)
    return frames
