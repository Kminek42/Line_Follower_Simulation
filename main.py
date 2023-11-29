import pygame
from graphic_engine import GraphicEngine
from track import Track
import numpy as np
import robot
from time import time
from learn import Network

pygame.init()

width, height = 1024, 768
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Open Polygon')

ge = GraphicEngine(screen, 1024, 768)
ge.camera_FOV = 6
ge.camera_pos = [0, 1]

genotype = np.array([ 1.19456666,  0.79075852,  1.53501633, -0.09641386,  1.20048471,
        0.70580301, -0.21671884, -1.88578059, -0.3363932 ])


net = Network(genotype, [8, 1])
r = robot.Robot(max_motor_speed=1, lenght=0.15, wheelbase=0.2, sensor_n=8, sensor_width=0.07, position=[0, -0.1], engine_cutoff=0.1)

t = Track()
t.add_segment("straight")
for i in range(35):
    t.add_segment("")

clock = pygame.time.Clock()
running = True
travelled_distance = 0
i = 0
s = 0
while running:
    screen.fill((0, 0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    inputs = np.array(r.get_sensors(t))
    e1, e2 = net.forward(inputs)
    s += r.move(e1, e2, 1/100)

    # print(travelled_distance)
    ge.draw_track(t)
    r.draw(ge)
    pygame.display.flip()
    clock.tick(60)


pygame.quit()
