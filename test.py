import math

sensors = []
x = 0      # position du robot (x global)
y = 10      # position du robot (y global)
angle = 90  # en degrés
width = 20
height = 40

# positions locales des capteurs (dans le repère du robot, origine au centre)
sensor_positions = [
    (-width*0.4, -height*0.4),
    (-width*0.2, -height*0.4),
    (0,          -height*0.4),
    (width*0.2,  -height*0.4),
    (width*0.4,  -height*0.4)
]

# convertir l'angle en radians pour le calcul trigonométrique
theta = math.radians(angle)

# transformation locale -> globale (rotation + translation)
for sx, sy in sensor_positions:
    # rotation
    rotated_x = sx * math.cos(theta) - sy * math.sin(theta)
    rotated_y = sx * math.sin(theta) + sy * math.cos(theta)

    # translation (ajouter position globale du robot)
    global_x = x + rotated_x
    global_y = y + rotated_y

    sensors.append((global_x, global_y))

print("Positions capteurs en coordonnées globales :")
for i, (gx, gy) in enumerate(sensors):
    print(f"Capteur {i+1} : ({gx:.2f}, {gy:.2f})")
