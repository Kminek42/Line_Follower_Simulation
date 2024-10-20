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

genotype = np.array([ 0.5203, -1.276 ,  0.1578,  0.6397, -1.6957, -0.2237, -0.5284,
       -0.9653,  0.7498, -1.8608, -1.6095, -0.6973,  0.191 ,  1.2007,
        0.3863, -0.7378,  0.3858,  0.3716, -0.3654,  1.1441,  0.1846,
       -1.4626,  0.6032, -3.6195,  0.8099,  0.0737,  0.1724,  1.3719,
        0.7616,  0.8463, -1.0053,  0.9619, -0.1375,  0.1176,  1.4903,
       -0.6218,  0.913 , -2.0223, -0.9431,  1.404 , -0.0186, -1.6735,
       -0.1339, -0.0776, -1.6706, -0.4326, -0.6592,  0.0039, -1.304 ,
       -1.0444, -0.5747, -0.4215,  0.1865, -0.0074,  0.7673, -1.1498,
        0.896 , -0.016 , -0.4847, -0.3642,  1.4052,  1.3923, -0.8806,
        0.0769, -0.3267,  0.9232,  1.7066,  0.8736,  0.0091, -0.3655,
        0.6491, -1.2229,  0.5363, -0.9147,  0.6205, -0.1609, -0.3883,
       -0.8855, -0.3567,  0.6016,  0.9855,  0.5264,  1.3639,  2.5392,
       -0.3245, -0.2059, -1.44  ,  1.1907,  1.2994, -0.8671,  0.6176,
        1.2171,  0.2263,  0.8474,  0.1748, -1.2169,  1.0493,  1.3251,
        0.7345, -0.9545, -0.7512, -1.1304, -0.3547,  1.2684,  0.4245,
        0.9405, -0.8676,  0.1459, -1.3699, -0.7718,  0.8787, -0.2396,
        1.2094, -0.4158,  2.7344, -0.831 , -1.4064, -0.0345, -0.7969,
        0.8469,  0.042 , -0.1373, -0.1241,  0.7403, -0.4525, -1.0009,
        1.0456, -0.2704, -0.926 , -0.513 ,  0.7101,  0.0925,  0.6301,
        1.7629,  0.231 , -0.8089,  1.0574,  0.0514,  0.8724, -0.8644,
       -0.959 ,  1.382 ,  0.9051, -0.6039,  0.3044,  0.2572,  0.0239,
        0.8719,  1.4374,  0.0073,  1.3309,  1.016 ,  0.2323,  0.1762])


c = robot_controller.RobotController(np.array([8, 8, 6, 4]), genotype[:170].reshape(1, -1), 2)

N=1
r = robot.Robot(
    number_of_robots=1,
    max_acceleration=6.0,
    max_speed=1.5,
    acceleration_coefficient=50.0,
    wheelbase=0.15,
    position=[0.0, 0.0],
    rotation=np.radians(90),
    sensor_positions=np.array([[0.15, 0.04], [0.17, 0.02], [0.15, 0.01], [0.15, -0.01], [0.17, -0.02], [0.15, -0.04]]),
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

