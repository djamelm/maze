import pygame
import math
import random
import imageio
import os
import asyncio
import platform

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1200, 600
TRACK_WIDTH = 800
GRAPH_WIDTH = 400
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moose Test PID Simulation")
clock = pygame.time.Clock()

# Define the Moose Test path
def line_path(x):
    """Generates a Moose Test-like path with sharp turns."""
    if x < 200:
        return HEIGHT // 2
    elif x < 400:
        return HEIGHT // 2 + (x - 200) * 0.5
    elif x < 600:
        return HEIGHT // 2 + 100 - (x - 400) * 0.5
    else:
        return HEIGHT // 2

# Robot class
class Robot:
    def __init__(self, x, y, color, kp=0.1, ki=0.0, kd=0.0):
        self.x = x
        self.y = y
        self.color = color
        self.angle = 0  # In degrees
        self.speed = 2  # px/frame
        self.width = 20
        self.height = 30
        self.sensor_positions = [(-8, -15), (-4, -15), (0, -15), (4, -15), (8, -15)]
        self.sensor_weights = [-2, -1, 0, 1, 2]
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.error = 0
        self.error_sum = 0
        self.last_error = 0
        self.path = [(x, y)]
        self.error_history = []

    def read_sensors(self, surface):
        """Simulate IR sensors reading the track."""
        total_error = 0
        for i, (dx, dy) in enumerate(self.sensor_positions):
            # Transform sensor position to world coordinates
            sensor_x = self.x + dx * math.cos(math.radians(self.angle)) - dy * math.sin(math.radians(self.angle))
            sensor_y = self.y + dx * math.sin(math.radians(self.angle)) + dy * math.cos(math.radians(self.angle))
            # Check pixel color at sensor position
            try:
                color = surface.get_at((int(sensor_x), int(sensor_y)))[:3]
                # Convert color to IR reading (0 on white, 1024 on black)
                intensity = 1024 if color == BLACK else 0
                total_error += intensity * self.sensor_weights[i]
            except IndexError:
                total_error += 1024 * self.sensor_weights[i]  # Out of bounds treated as black
        return total_error / len(self.sensor_positions)

    def update(self, surface, dt):
        """Update robot position using PID control."""
        self.error = self.read_sensors(surface)
        self.error_sum += self.error * dt
        error_diff = (self.error - self.last_error) / dt if self.last_error is not None else 0
        self.last_error = self.error

        # PID control
        correction = self.kp * self.error + self.ki * self.error_sum + self.kd * error_diff
        self.angle += correction * dt  # Adjust angle based on PID

        # Update position
        self.x += self.speed * math.cos(math.radians(self.angle)) * dt
        self.y += self.speed * math.sin(math.radians(self.angle)) * dt
        self.path.append((self.x, self.y))
        self.error_history.append(self.error)
        if len(self.error_history) > GRAPH_WIDTH:
            self.error_history.pop(0)

    def draw(self, surface):
        """Draw the robot and its direction arrow."""
        # Draw robot body
        points = [
            (self.x + self.width / 2 * math.cos(math.radians(self.angle)) - self.height / 2 * math.sin(math.radians(self.angle)),
             self.y + self.width / 2 * math.sin(math.radians(self.angle)) + self.height / 2 * math.cos(math.radians(self.angle))),
            (self.x + self.width / 2 * math.cos(math.radians(self.angle)) + self.height / 2 * math.sin(math.radians(self.angle)),
             self.y + self.width / 2 * math.sin(math.radians(self.angle)) - self.height / 2 * math.cos(math.radians(self.angle))),
            (self.x - self.width / 2 * math.cos(math.radians(self.angle)) + self.height / 2 * math.sin(math.radians(self.angle)),
             self.y - self.width / 2 * math.sin(math.radians(self.angle)) - self.height / 2 * math.cos(math.radians(self.angle))),
            (self.x - self.width / 2 * math.cos(math.radians(self.angle)) - self.height / 2 * math.sin(math.radians(self.angle)),
             self.y - self.width / 2 * math.sin(math.radians(self.angle)) + self.height / 2 * math.cos(math.radians(self.angle)))
        ]
        pygame.draw.polygon(surface, self.color, points)

        # Draw sensors
        for dx, dy in self.sensor_positions:
            sensor_x = self.x + dx * math.cos(math.radians(self.angle)) - dy * math.sin(math.radians(self.angle))
            sensor_y = self.y + dx * math.sin(math.radians(self.angle)) + dy * math.cos(math.radians(self.angle))
            pygame.draw.circle(surface, RED, (int(sensor_x), int(sensor_y)), 2)

        # Draw direction arrow proportional to PID correction
        arrow_length = abs(self.error) * 0.05
        arrow_end_x = self.x + arrow_length * math.cos(math.radians(self.angle))
        arrow_end_y = self.y + arrow_length * math.sin(math.radians(self.angle))
        pygame.draw.line(surface, GREEN, (self.x, self.y), (arrow_end_x, arrow_end_y), 2)

    def reset(self, x, y):
        """Reset robot to initial position."""
        self.x = x
        self.y = y
        self.angle = 0
        self.error = 0
        self.error_sum = 0
        self.last_error = 0
        self.path = [(x, y)]
        self.error_history = []

# Draw the track
def draw_track(surface):
    surface.fill(BLACK)
    for x in range(TRACK_WIDTH):
        y = int(line_path(x))
        pygame.draw.rect(surface, WHITE, (x, y - 10, 1, 20))

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

# Main game loop
async def main():
    robot1 = Robot(50, HEIGHT // 2, BLUE, kp=0.1, ki=0.0, kd=0.0)
    robot2 = Robot(50, HEIGHT // 2 + 30, ORANGE, kp=0.05, ki=0.0, kd=0.0)
    recording = False
    frames = []
    running = True
    dt = 1.0 / FPS

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Robot 1 PID controls
                if event.key == pygame.K_q:
                    robot1.kp += 0.01
                elif event.key == pygame.K_a:
                    robot1.kp = max(0, robot1.kp - 0.01)
                elif event.key == pygame.K_w:
                    robot1.ki += 0.001
                elif event.key == pygame.K_s:
                    robot1.ki = max(0, robot1.ki - 0.001)
                elif event.key == pygame.K_e:
                    robot1.kd += 0.01
                elif event.key == pygame.K_d:
                    robot1.kd = max(0, robot1.kd - 0.01)
                # Robot 2 PID controls
                elif event.key == pygame.K_u:
                    robot2.kp += 0.01
                elif event.key == pygame.K_j:
                    robot2.kp = max(0, robot2.kp - 0.01)
                elif event.key == pygame.K_i:
                    robot2.ki += 0.001
                elif event.key == pygame.K_k:
                    robot2.ki = max(0, robot2.ki - 0.001)
                elif event.key == pygame.K_o:
                    robot2.kd += 0.01
                elif event.key == pygame.K_l:
                    robot2.kd = max(0, robot2.kd - 0.01)
                # Other controls
                elif event.key == pygame.K_r:
                    robot1.reset(50, HEIGHT // 2)
                    robot2.reset(50, HEIGHT // 2 + 30)
                elif event.key == pygame.K_F1:
                    pygame.image.save(screen, "screenshot.png")
                elif event.key == pygame.K_F2:
                    recording = not recording
                    if not recording and frames:
                        imageio.mimsave("simulation.gif", frames, fps=FPS)
                        frames = []
                elif event.key == pygame.K_ESCAPE:
                    running = False

        # Update
        draw_track(screen)
        robot1.update(screen, dt)
        robot2.update(screen, dt)

        # Draw
        robot1.draw(screen)
        robot2.draw(screen)
        # Draw paths
        if len(robot1.path) > 1:
            pygame.draw.lines(screen, BLUE, False, robot1.path, 2)
        if len(robot2.path) > 1:
            pygame.draw.lines(screen, ORANGE, False, robot2.path, 2)
        draw_pid_graph(screen, robot1, robot2)
        draw_hud(screen, robot1, robot2)

        # Record frame if needed
        if recording:
            frame = pygame.surfarray.array3d(screen)
            frame = frame.transpose([1, 0, 2])  # Convert to correct format
            frames.append(frame)

        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(1.0 / FPS)

    pygame.quit()

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())