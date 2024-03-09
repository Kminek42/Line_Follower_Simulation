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

genotype = np.array([-0.665 , -0.4064,  0.3496,  1.1792, -0.6548,  0.079 ,  0.3094,
       -0.4249,  0.6546, -0.4119, -0.6511, -1.9643,  0.7146, -1.053 ,
       -0.1343, -0.9965,  1.1333,  0.1818, -0.3996, -0.2789,  1.337 ,
        0.388 ,  0.2245, -0.1306, -0.6019, -2.2885, -2.3171,  0.0785,
        0.5716, -0.305 , -0.4139,  0.5495, -1.2472,  1.1011,  0.0961,
       -1.0189, -0.6519, -0.3674,  0.8519, -1.7931,  1.0108,  2.1123,
        0.7447, -0.3706,  0.4099, -0.0799,  0.5058,  0.4355, -0.3477,
        1.7787, -0.5512, -0.0893, -1.5652, -0.1358,  0.3105,  0.4102,
        0.9794,  0.0919, -1.4848,  1.0558,  1.5616, -0.5651, -1.6397,
       -0.6719, -1.7743, -0.568 , -0.1652,  0.5188, -1.3745,  0.0537,
       -0.013 , -0.6396,  0.518 , -0.1892, -2.2469,  0.2119, -0.4203,
       -0.5507,  0.1337,  0.3719,  1.0629,  0.1862,  0.1936, -0.3247,
        0.0033, -0.2205, -1.195 , -0.7746, -0.0252,  1.8627, -1.1128,
        0.4006,  0.0788,  1.6962,  0.7973, -1.4169, -0.5085,  0.8702,
        0.5372, -1.294 ,  0.1092,  0.6256,  1.7095,  0.1033,  0.3293,
        0.1697,  0.3975,  1.4336, -2.7579,  2.5041, -1.3712,  0.5547,
        0.8058,  0.8209,  0.7918,  0.1709,  0.1753, -0.8508,  0.2877,
        0.3788,  0.2431, -0.6529, -0.1357,  2.9969, -1.8222, -0.3104,
        0.0868, -0.4919, -2.2156,  1.6225, -0.0601, -1.0597,  0.7901,
        1.1104, -0.9552,  1.0795, -0.3934,  0.9088, -1.0825, -0.5808,
       -0.7772,  1.4051,  1.7588, -0.898 , -0.1856, -0.2473, -1.1711,
       -0.2507, -0.3531, -0.5482, -0.2813, -0.6498, -0.6931, -0.5835,
       -1.2774, -0.6997,  0.1219,  0.6031,  0.5858,  0.2868,  0.1991,
       -0.8961,  0.2185,  0.3075, -0.2985, -0.3543, -0.0327,  0.1978,
        1.4233,  1.7181])


c = robot_controller.RobotController4(genotype[:170])

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
    screen.fill((0, 0, 0))

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

