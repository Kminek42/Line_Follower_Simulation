import pygame
from graphic_engine import GraphicEngine
from track import Track
import numpy as np
import robot
import robot_controller
import matplotlib.pyplot as plt

pygame.init()

width, height = 1024, 768
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Open Polygon')

ge = GraphicEngine(screen, 1024, 768)
ge.camera_FOV = 8
ge.camera_pos = [0, 3.5]

genotype = np.array([-1.71857719,  0.24561643, -0.20897476,  1.36194922,  1.53502913,
        0.56644004,  0.14926509,  2.38201   , -0.76570219])


c = robot_controller.RobotController2(genotype)
# c.set_mode(False)
r = robot.Robot(max_motor_speed=1)

t = Track(tile_size=0.25)
t.add_segment("straight")
for i in range(40):
    t.add_segment("")

clock = pygame.time.Clock()
running = True
travelled_distance = 0
i = 0
s = 0
dt = 1/200

X = []
Y = []

s_a = 0
s_c = 6e-2

while running:
    screen.fill((0, 0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    inputs = np.array(r.get_sensors(t))
    e1, e2 = c.get_motors(inputs)
    motor_l = np.max([np.min([1, e1]), -1])
    motor_r = np.max([np.min([1, e2]), -1])
    print(motor_r - motor_l)
    s_a += s_c * ((motor_r - motor_l) - s_a)
    Y.append(s_a)
    ds = r.move(e1, e2, dt)
    s += ds
    #print(np.round(ds / dt, 2))
    ge.draw_track(t)
    r.draw(ge)
    pygame.display.flip()
    clock.tick(60)


pygame.quit()

plt.plot(Y)
plt.show()
