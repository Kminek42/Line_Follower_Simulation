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

genotype = np.array([ 0.8811,  1.5058,  2.4298,  1.3652, -0.6874,  0.7662,  0.3284,
       -0.9752, -0.4677, -1.9618,  1.2676, -0.3375,  0.6181, -1.7168,
        1.3525, -0.1887, -0.7135, -1.0868, -0.3902, -0.4701,  0.4091,
        0.3526,  0.0301, -1.2455, -0.1879,  0.43  , -0.4236, -0.6232,
       -0.1925,  0.2666,  0.9213,  0.9549,  0.8109, -0.4246,  1.038 ,
        0.2687, -1.376 ,  0.9212, -1.2039, -0.5486, -0.5565,  0.543 ,
       -0.0758,  0.8727, -1.881 ,  0.6715,  0.8589, -0.2697,  0.3304,
       -1.1453,  1.3349,  0.8316,  0.0015, -1.9378, -0.7604, -0.2241,
        0.4569,  0.5063, -0.5606, -0.5473,  1.4372,  0.4688,  0.9347,
        0.4192, -0.2981,  0.9686,  0.2333,  0.0795,  1.5238,  0.1092,
        0.7186, -0.9045, -0.1869,  1.8642, -0.5726, -0.9101,  0.3084,
       -1.8273,  0.2182,  0.9106,  1.0553,  0.6536, -0.1547, -0.0033,
        2.3743,  1.754 , -0.4128,  0.25  , -0.3881, -0.6684,  0.7356,
       -1.3096, -1.9138,  0.9413,  1.0102,  0.1274, -0.3614, -0.2385,
       -2.5818, -0.626 , -0.6929, -0.4135,  0.3258, -0.5452, -2.5028,
        0.6846,  3.0984, -0.0849,  0.5481,  0.2736, -0.724 , -0.3345,
        0.0367,  0.2075,  0.0631,  1.6103,  0.0145, -0.7617, -0.9808,
       -1.002 ,  0.0742, -2.741 , -0.4586, -0.3067, -1.5243,  0.7977,
       -1.1391,  0.595 ,  2.7838, -0.6376,  1.0446, -0.4075, -0.2972,
        0.7603,  1.1063,  0.7716, -0.313 ,  2.4338, -1.7702, -0.0667,
        0.1697,  0.0894,  0.488 , -0.0544, -0.1199,  0.1137,  0.7828,
        0.5883, -0.3185, -0.3124,  0.5435,  1.0349, -2.2081,  0.3608,
       -0.1359,  0.9476,  1.3854, -0.6641, -0.6764, -2.2303,  1.0516,
       -0.8435, -1.5803,  0.0161, -0.3657,  0.8231,  0.8924,  0.0956,
        0.0636,  0.2869])


c = robot_controller.RobotController(np.array([10, 8, 6, 4]), genotype.reshape(1, -1), 2)

N=1
r = robot.Robot(
    number_of_robots=1,
    max_acceleration=10.0,
    max_speed=1.5,
    acceleration_coefficient=50.0,
    wheelbase=0.15,
    position=[0.0, 0.0],
    rotation=np.radians(90),
    sensor_positions=np.array([0.15, 0]) + np.array([
        [0.0, 0.03],
        [0.0, 0.01],
        [0.0, -0.01],
        [0.0, -0.03],
        [0.02, 0.03],
        [0.02, 0.01],
        [0.02, -0.01],
        [0.02, -0.03],
    ]),
    sensor_noise=0.0,
    sensor_radius=0.005,
    track_width=0.018
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

    sensors = r.get_sensors(t)
    print(np.round(sensors, 1))
    r.move(c.get_motors(sensors), dt)
    # r.move(np.array([[1, .1]]), dt)
    ge.draw_track(t)
    r.draw(ge)
    pygame.display.flip()
    clock.tick(60)


pygame.quit()

