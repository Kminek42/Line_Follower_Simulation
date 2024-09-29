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

genotype = np.array([ 0.0991,  1.7118,  0.5838, -2.0967,  2.1391, -0.2988, -0.3595,
        1.0817,  1.9048,  0.0323,  1.3133,  1.8277,  0.0033, -0.2747,
       -1.8838, -0.4496, -0.1714, -1.7716, -1.7346, -1.4998,  0.1201,
       -0.1003,  0.3785, -0.4296,  0.6418, -0.5795,  0.9597,  0.8988,
       -1.6469,  0.3597, -0.5044,  0.5269, -0.7402, -1.7359, -0.2203,
       -0.3602,  1.8286,  0.3204, -0.3991,  0.5681, -0.7159, -0.5439,
        0.8313, -0.1886, -0.3026,  1.4196,  0.854 , -0.7469,  0.0331,
        1.1992, -2.1791, -1.127 ,  1.4042,  0.2929,  1.8003, -0.0843,
        0.5359, -2.5716,  0.6395,  0.3971, -1.0248, -0.7394, -0.3573,
       -1.5151,  1.017 ,  0.2076,  0.9467, -0.3671,  0.9429, -0.48  ,
        0.422 , -0.5708,  0.5358, -0.8256,  0.4033,  0.153 ,  1.1671,
        1.0048,  0.0589,  0.306 ,  1.6508, -0.5989,  0.4551, -0.114 ,
       -0.496 ,  0.7765, -0.2272, -1.1736, -1.5241,  0.0893, -0.8718,
        1.5487, -0.3891,  0.4354,  0.8399, -0.8987, -1.2606, -2.0237,
       -0.1257,  1.2962, -1.2737,  0.5553,  1.4272,  0.2482, -0.1434,
       -0.0143,  0.2377,  0.4828, -0.5739, -0.1462, -1.4771,  0.6844,
       -0.3598,  0.6623, -0.0135, -0.6199, -1.1654, -0.9712, -1.4476,
        0.1006,  0.2784,  1.0366, -0.2017, -2.1284, -0.6893, -1.1202,
       -0.844 , -0.6952,  0.0635, -0.8101, -0.322 , -0.4165,  0.3332,
        0.3888, -1.6895,  0.1933, -0.2918, -0.7877,  1.6117, -0.924 ,
        0.2972, -0.4633, -0.0889, -0.6887, -0.0636, -0.3719, -1.4158,
        0.96  , -1.6123, -0.7408,  0.352 ,  0.2487,  1.209 , -1.4415,
        0.3941, -0.1289, -0.1864, -0.0508, -0.363 ,  0.2518, -0.7289,
        0.8951,  0.9759, -1.5894, -1.5764,  0.1388,  1.5604,  0.1286,
       -0.1365,  0.5402])


c = robot_controller.RobotController(genotype[:170])

N=1
r = robot.Robot(
        max_motor_speed=1.0,
        wheelbase=[0.2],
        lenght=[0.14],
        engine_acceleration=10.0,
        rotation=np.pi/2,
        sensor_width=[0.067],
        sensor_n=8,
        sensor_noise=0.1,
        sensor_radius=0.005,
        min_speed=0.1,
        position=[0.0, 0.0],
        track_width=0.02
    )
t = Track(tile_size=0.25)
t.add_segment("straight")
for i in range(20):
    t.add_segment("")
t.add_segment("straight")
t.finalize(128)

clock = pygame.time.Clock()
running = True

dt = 1/200

while running:
    ge.clear_screen()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    sensors = np.array(r.get_sensors(t)[0])
    inputs = np.array(sensors)
    e1, e2 = c.get_motors(inputs)
    # print(sensors)
    r.move([e1], [e2], dt)
    # print(np.round(sensors, 2))
    ge.draw_track(t)
    r.draw(ge)
    pygame.display.flip()
    clock.tick(60)


pygame.quit()

