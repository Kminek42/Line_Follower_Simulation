import pygame
from graphic_engine import GraphicEngine
from track import Track
import numpy as np
import robot
from time import time

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Open Polygon')

ge = GraphicEngine(screen, 800, 600)
ge.camera_FOV = 3
ge.camera_pos = [0, 1]
t = Track()
r = robot.Robot(max_motor_speed=1, lenght=0.15, wheelbase=0.2, sensor_n=8, sensor_width=0.07)
w = np.array([
[ 0.90442527, -0.55865717],
[-0.96039851,  0.23967487],
 [-0.71714972,  0.03450054],
 [ 0.8082427,  -0.22964068],
 [-0.03806513,  0.88206087],
 [ 0.92759926,  0.26424767],
 [ 0.26563596,  0.91853224],
 [-0.08262744, -0.62194546]])

t.add_segment("straight")
for i in range(40):
    t.add_segment("")

clock = pygame.time.Clock()
running = True
travelled_distance = 0
i = 0
while running:
    screen.fill((0, 0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    inputs = np.array(r.get_sensors(t))
    print(inputs.shape, w.shape)
    outputs = inputs @ w
    e1 = outputs[0]
    e2 = outputs[1]
    travelled_distance += r.move(e1, e2, 1/60)
    # print(travelled_distance)
    ge.draw_track(t)
    r.draw(ge)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
