import pygame
from graphic_engine import GraphicEngine
from track import Track
import numpy as np
import robot
import robot_controller
import matplotlib.pyplot as plt
from time import time

pygame.init()

width, height = 1024, 768
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Open Polygon')

ge = GraphicEngine(screen, 1024, 768)
ge.camera_FOV = 5
ge.camera_pos = [0, 2]

genotype = np.array([-1.00235109,  0.04736482,  1.46274045, -0.71693161,  0.56644004,
        0.13274981, -0.70470132,  1.39547227,  1.78748405, -0.77161791,
        0.17538653, -0.46250554, -1.0858006 , -0.8378228 , -0.38586334,
       -0.77576235,  0.99571135, -1.93320478,  0.24853063,  2.13154737,
       -0.13947396,  0.36311122,  0.44863753, -0.99242977, -0.22593966,
       -1.65457077, -0.63972264, -0.4794198 , -0.36844052, -0.77602047,
       -0.30736481, -0.36652394,  1.11971196, -0.45792242,  0.4253934 ,
        0.41484383,  1.47598983, -0.35924111,  1.17526124, -0.67877739,
       -0.35362786, -0.34224423,  0.11677341, -0.21290758,  0.61980106,
        1.79116846,  1.16920558, -1.72567135,  0.16065854, -0.85898532,
       -0.20642094,  0.48842647,  1.07029911,  0.93455847, -0.99090328,
        0.32889807,  0.3415874 , -1.25088622,  0.92525075, -0.90478616,
        1.84369153, -0.52047649, -1.44553558,  0.37716061,  0.77455994,
        0.60415971, -0.45547928,  0.12162495,  1.99079554, -0.34143963,
        0.93755884, -0.25460809, -0.45031425,  0.20728277,  1.09964197,
        0.93989698,  0.42379221, -0.71383018,  0.56688187,  1.87239408,
       -0.07524683,  0.05334491,  1.03081595, -0.00350885,  0.01745159,
       -1.49011141, -1.070215  ,  0.54762261, -1.18478941, -1.066637  ,
       -1.12112324,  1.33697117,  1.74303872, -0.32187919,  0.82957109,
       -0.18737662,  1.11799861, -1.11278278,  1.15132983, -0.77245771,
       -0.22157935, -1.1452478 ,  0.20918977, -0.48567617, -0.32319528,
        0.56705637,  1.06783358,  0.27159574, -0.69441932, -0.058626  ,
       -0.3462066 ,  0.2967472 ,  0.62645686, -1.05317438, -0.63947627,
       -0.14852688, -1.57458215, -0.4956882 , -0.11757479, -0.74568761,
       -0.38602877, -1.29696041, -1.95827161, -0.47886222,  0.5797988 ,
       -3.31215179, -0.71952667, -0.26834519, -0.80811606, -0.71891095,
       -0.15747041, -0.38367719, -0.11393189,  0.07285698,  0.53444558,
        0.10003728,  0.42808095, -1.03978785,  1.27180126, -0.0057689 ,
        0.7960705 , -1.25985549, -1.58544491,  0.28614781, -0.60414894,
        0.90332566,  1.51347609, -2.10082473,  1.00607292, -0.80889613,
       -0.95869292, -1.10219609,  1.0785791 ,  0.02156289,  0.13265776,
       -0.72592119,  0.75520898, -0.87912447,  0.40948504, -0.10427863,
       -0.83176428,  0.58979914, -0.47546082,  0.78506445, -0.82646112,
        0.78420863,  0.71911832, -1.26459544,  0.85693318, -0.49399435])


c = robot_controller.RobotController4(genotype)
# c.set_mode(False)
r = robot.Robot(max_motor_speed=1.0)
t = Track(tile_size=0.25)
t.add_segment("straight")
for i in range(20):
    t.add_segment("")
t.add_segment("straight")

clock = pygame.time.Clock()
running = True
travelled_distance = 0
i = 0
s = 0
dt = 1/200

X = []
Y = []

s_a = 0
s_c = 1e-1
s_r = 0

while running:
    screen.fill((0, 0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    t0 = time()
    sensors = np.array(r.get_sensors(t))
    inputs = np.array(sensors)
    e1, e2 = c.get_motors(inputs)
    # print(e1, e2)
    ds = r.move(e1, e2, dt)
    t0 = time() - t0
    print(t0)
    s += ds
    print(np.round(ds / dt, 3))
    ge.draw_track(t)
    r.draw(ge)
    pygame.display.flip()
    clock.tick(60)


pygame.quit()
