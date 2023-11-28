import pygame
from graphic_engine import GraphicEngine
from track import Track
import numpy as np
import robot
from time import time
from learn import Network

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Open Polygon')

ge = GraphicEngine(screen, 800, 600)
ge.camera_FOV = 6
ge.camera_pos = [0, 1]


w1 = np.array([[ 0.0369184 ,  0.10525324, -0.07193377, -0.48344666],
       [ 2.23112292,  0.53097061, -0.32521209,  0.2320492 ],
       [ 0.71662317,  2.04525242,  0.26745555,  0.98377448],
       [ 0.55155775,  0.01668726, -0.0327905 ,  2.24457364],
       [ 0.70578746, -0.55612778,  2.24594008, -1.6007702 ],
       [ 0.93701096, -0.51345321, -0.33925233,  1.50418325],
       [ 0.68642338, -1.44414332,  0.59936675, -0.94906993],
       [-0.21398832,  0.14605547, -0.98294605, -0.46458507],
       [ 0.18650391, -0.63992111, -1.06668243,  0.75731341]])

w2 = np.array([[ 1.51446528, -0.3576823 ,  1.76784614],
       [-1.12115099,  1.19909128, -0.6687727 ],
       [ 2.26649579,  0.35408288, -0.02292686],
       [ 0.04199896,  1.41332062,  1.09740199]])

b1 = np.array([ 0.37678953, -0.58113617, -0.59270863, -0.9042974 ])

b2 = np.array([-0.08474405,  1.27970495, -0.17627286])


net = Network(w1, w2, b1, b2)
robot = robot.Robot(max_motor_speed=1, lenght=0.15, wheelbase=0.2, sensor_n=8, sensor_width=0.07)

t = Track()
t.add_segment("straight")
t.add_segment("90_left")
t.add_segment("straight")
t.add_segment("x-intersection")
t.add_segment("straight")
t.add_segment("90_right")
t.add_segment("straight")
for i in range(31):
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

    inputs = np.array(robot.get_sensors(t))
    e1, e2 = net.forward(inputs)
    s += robot.move(e1, e2, 1/100)

    travelled_distance += robot.move(e1, e2, 1/100)
    # print(travelled_distance)
    ge.draw_track(t)
    robot.draw(ge)
    pygame.display.flip()
    clock.tick(60)


pygame.quit()
