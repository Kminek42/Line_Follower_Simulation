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

genotype = np.array([-0.2709, -1.3073, -0.2461, -1.8615, -0.1833, -1.0654, -1.6052,
        0.2076, -0.0936,  0.0305, -0.6689,  0.6824, -0.4631, -2.8843,
       -0.2556, -0.2198, -0.6722,  1.2664, -0.14  ,  0.8552,  0.5566,
       -1.993 , -0.3988,  0.9662, -0.2374,  1.4855, -0.2686, -0.7109,
       -1.2949,  1.5186, -0.3114, -2.0515, -0.4266, -0.0184, -0.3773,
       -0.4657, -2.1909,  0.1592,  0.4845,  1.5966,  0.1937,  0.4706,
        1.4655,  0.1261,  2.2065,  0.3516,  0.2991, -0.2393, -0.547 ,
        0.7768,  0.1953,  1.5244, -0.4864, -0.3465, -0.4568,  0.0372,
       -1.0451, -0.3807,  1.1542,  0.4226,  1.2939, -0.1461, -0.67  ,
        0.0163, -0.9115,  0.1661, -0.164 ,  0.202 , -0.244 ,  0.9505,
        0.5089,  2.3568,  0.1222, -0.8388, -0.9176,  0.1707,  0.0384,
        0.5205, -0.7163,  0.7496,  1.1996,  0.8812, -1.5531, -0.3806,
       -0.7896, -0.2281, -0.8146, -0.2229, -1.1476,  0.4225,  1.4291,
        0.9441,  0.2573, -1.7642,  0.735 , -1.9163,  1.8463, -0.2133,
       -0.64  , -0.4244, -0.7638, -3.0902, -2.8771,  0.6509,  0.5054,
        0.1958,  2.1878,  2.0316,  0.5914,  1.1469, -0.4285, -0.1348,
       -0.9627,  1.1176, -0.8013, -0.125 ,  1.4225,  0.7127, -0.1608,
       -0.3966,  1.5753,  0.9817, -0.4684,  0.1356, -0.7769,  0.6127,
        0.9289,  2.2724, -1.4433, -0.6632,  0.1491, -0.3723,  0.8247,
        0.9432,  0.1025,  0.2163,  0.5661,  0.14  , -0.6268,  1.4236,
       -0.6453, -1.4714,  0.5726, -0.0059, -1.0467,  0.924 , -0.5023,
       -0.4928, -0.116 , -0.9825,  0.392 ,  1.7127,  0.3877,  0.9073,
        0.7653,  1.0488,  0.0151,  0.3384,  0.1272,  0.7307,  0.5027,
       -0.9631,  1.2092,  0.9414,  1.9094,  0.8099, -0.2167,  0.2356,
        0.6506,  1.7181])


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
        sensor_noise=0.05,
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

