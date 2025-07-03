
# Capture
def save_screenshot():
    filename = f"screenshot_{datetime.now().strftime('%H%M%S')}.png"
    pygame.image.save(SCREEN, filename)
    

    
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

                
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Gestion du clavier
            if event.type == pygame.KEYDOWN:
                # Réglages PID robot1
                if event.key == pygame.K_q:  # Kp +
                    robot1.pid.kp += 0.01
                elif event.key == pygame.K_a:  # Kp -
                    robot1.pid.kp = max(0, robot1.pid.kp - 0.01)
                elif event.key == pygame.K_w:  # Ki +
                    robot1.pid.ki += 0.0001
                elif event.key == pygame.K_s:  # Ki -
                    robot1.pid.ki = max(0, robot1.pid.ki - 0.0001)
                elif event.key == pygame.K_e:  # Kd +
                    robot1.pid.kd += 0.01
                elif event.key == pygame.K_d:  # Kd -
                    robot1.pid.kd = max(0, robot1.pid.kd - 0.01)
                
                # Réglages PID robot2
                elif event.key == pygame.K_u:  # Kp +
                    robot2.pid.kp += 0.01
                elif event.key == pygame.K_j:  # Kp -
                    robot2.pid.kp = max(0, robot2.pid.kp - 0.01)
                elif event.key == pygame.K_i:  # Ki +
                    robot2.pid.ki += 0.0001
                elif event.key == pygame.K_k:  # Ki -
                    robot2.pid.ki = max(0, robot2.pid.ki - 0.0001)
                elif event.key == pygame.K_o:  # Kd +
                    robot2.pid.kd += 0.01
                elif event.key == pygame.K_l:  # Kd -
                    robot2.pid.kd = max(0, robot2.pid.kd - 0.01)
                
                # Commandes générales
                elif event.key == pygame.K_r:  # Reset
                    robot1.reset(50, HEIGHT // 2, 0)
                    robot2.reset(50, HEIGHT // 2 - 40, 0)
                    errors1 = []
                    errors2 = []
                elif event.key == pygame.K_F1:  # Capture d'écran
                    pygame.image.save(screen, "moose_test_simulation.png")
                elif event.key == pygame.K_ESCAPE:  # Quitter
                    running = False
                    
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

                    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    robot1.reset(100, 400)
                    robot2.reset(100, 450)
                elif event.key == pygame.K_F1:
                    pygame.image.save(screen, f"capture_{time.time()}.png")
                elif event.key == pygame.K_F2:
                    recording = not recording
                    if not recording and frames:
                        # Sauvegarder l'animation GIF
                        imageio.mimsave('simulation.gif', frames, fps=10)
                        frames = []

                # Ajustement des paramètres PID pour le robot 1
                elif event.key == pygame.K_q:
                    robot1.Kp += 0.1
                elif event.key == pygame.K_a:
                    robot1.Kp -= 0.1
                elif event.key == pygame.K_w:
                    robot1.Ki += 0.01
                elif event.key == pygame.K_s:
                    robot1.Ki -= 0.01
                elif event.key == pygame.K_e:
                    robot1.Kd += 0.1
                elif event.key == pygame.K_d:
                    robot1.Kd -= 0.1

                # Ajustement des paramètres PID pour le robot 2
                elif event.key == pygame.K_u:
                    robot2.Kp += 0.1
                elif event.key == pygame.K_j:
                    robot2.Kp -= 0.1
                elif event.key == pygame.K_i:
                    robot2.Ki += 0.01
                elif event.key == pygame.K_k:
                    robot2.Ki -= 0.01
                elif event.key == pygame.K_o:
                    robot2.Kd += 0.1
                elif event.key == pygame.K_l:
                    robot2.Kd -= 0.1

                    
def save_screenshot():
    """Enregistre une capture d'écran"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    pygame.image.save(screen, filename)
    print(f"Capture sauvegardée : {filename}")

    
        # Enregistrement GIF
        if recording:
            frame = pygame.surfarray.array3d(screen)
            frame = frame.swapaxes(0, 1)
            frames.append(frame)