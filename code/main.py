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
ge.camera_FOV = 4
ge.camera_pos = [0, 2]
genotype = np.array([-0.1784,  0.0179,  0.2625, -0.9068,  0.5541, -3.2434,  0.9347,
       -1.5288, -0.078 , -2.0985, -0.1069, -1.7554,  1.8696,  0.014 ,
       -1.2842, -0.9586, -0.4208, -0.4771,  0.8711, -0.0847,  2.2229,
        0.537 , -1.3666, -1.2818,  0.2401, -0.3742, -1.0425,  1.3803,
       -0.5459,  0.8617, -0.6577, -3.014 ,  1.5119,  0.9313, -1.6674,
        0.0007, -0.7632,  0.8259, -1.397 , -0.5493, -0.615 , -0.9921,
        0.4721,  1.0706,  2.0235, -0.395 ,  1.3284,  1.134 ,  1.5095,
       -1.2632,  0.4927,  0.283 , -1.2011,  0.6941,  0.2297, -1.2538,
        0.1449,  0.8308,  0.3912,  0.284 , -1.3308,  1.0676,  1.945 ,
       -1.5945,  1.3434,  0.5098,  0.2267, -2.0783, -0.8252, -0.0703,
        0.4888, -1.5007, -1.35  , -0.9342, -0.211 ,  1.0118, -0.9732,
       -0.6228, -1.2917, -0.0944, -0.6026,  1.4696, -1.0149, -0.9227,
       -0.1288,  1.2585,  0.272 , -1.1317, -0.195 ,  0.0017, -1.3671,
       -0.7176, -0.0438,  0.6938,  2.3899,  2.9678, -1.2583, -0.5829,
       -0.4739, -0.131 , -0.371 ,  2.1003,  0.093 ,  0.4474, -0.1288,
       -0.3203,  0.8836, -1.5264,  0.1075, -0.8738,  1.3699, -0.4926,
        1.0724, -0.6077,  0.3124,  1.1472, -0.7037, -0.6948, -0.275 ,
       -0.6972, -0.8628,  0.6991, -0.0855,  0.0488,  0.9327,  0.9302,
       -0.0447, -0.8046, -0.2072,  0.2781,  0.8842,  0.0738, -0.6539,
       -0.2327,  1.5702, -1.1942,  0.3635, -0.151 , -1.9968,  1.0385,
        0.4831, -1.6677,  0.7313, -0.0918,  0.8222, -1.532 ,  0.3668,
       -0.5125, -0.3273, -0.9754,  1.2898, -0.0034, -0.5043,  0.7498,
       -0.1562,  0.5282,  0.6177,  1.3425,  0.9567,  0.4736,  0.7814,
       -1.5792, -0.5396, -0.3071, -0.3499, -0.8143, -1.6813,  1.2231,
       -1.4469, -0.601 ,  1.0187, -0.4481, -1.549 , -1.5856, -1.1965,
       -0.6067,  1.0473, -0.0569,  0.0884,  0.7412, -0.8843, -1.2169,
        0.5921, -0.2329,  0.196 ,  1.1933,  1.3716,  0.4181,  1.8338,
       -1.1329,  0.2441, -1.8977, -0.5782, -1.1176, -1.0702,  0.7317,
        0.8365,  0.4388, -0.9069,  0.7146,  0.4727,  1.3215,  0.2081,
       -0.6133,  0.5359,  0.0521, -0.8817, -0.182 ,  0.4783, -0.9827,
        0.621 ,  0.1748,  0.0796,  0.6471, -0.1569, -0.0498,  0.3188,
       -1.65  ])


c = robot_controller.RobotController(np.array([11, 9, 7, 5]), genotype.reshape(1, -1), 3)

child_n=1
r = robot.Robot(
    number_of_robots=child_n,
    max_acceleration=25.0,
    max_speed=1.0,
    acceleration_coefficient=50.0,
    wheelbase=0.2,
    position=[0.0, 0.0],
    rotation=np.radians(90),
    sensor_positions=np.array([0.14, 0]) + np.array(np.meshgrid(np.linspace(0.0, 0.0, 1), np.linspace(-0.033, 0.033, 8))).T.reshape(-1, 2),
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
    motors = c.get_motors(sensors)
    print(np.round(sensors, 1).reshape(-1, 8), np.round(motors, 2))
    r.move(motors, dt)
    # r.move(np.array([[1, .1]]), dt)
    ge.draw_track(t)
    r.draw(ge)
    pygame.display.flip()
    clock.tick(60)


pygame.quit()

