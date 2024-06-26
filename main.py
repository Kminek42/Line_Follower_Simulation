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

genotype = np.array([-0.6043, -1.5689, -0.5284, -0.3657,  0.1828,  1.1211,  0.1907,
        0.2081,  0.3844, -1.7549, -1.6625, -1.497 , -0.3733, -1.8717,
       -0.6898, -1.3682,  1.6557,  0.4377, -0.9369, -1.9   , -0.2371,
        0.3286,  0.8107,  1.7534,  1.1185,  0.1648, -0.2852, -0.7429,
        1.3557,  0.1666,  0.6305, -0.6904, -1.2409, -0.4003, -0.3029,
        0.1918, -0.7374,  0.025 ,  1.1777, -1.673 , -2.1169,  1.2459,
        1.54  , -1.3545,  0.5131, -0.0592, -0.0733, -1.2789,  2.5187,
        1.7806, -0.6937,  1.0509,  0.5055, -0.0195, -0.9079,  0.4514,
       -0.306 , -0.3796, -0.7671,  0.9998, -0.7677, -1.7586, -0.8726,
        0.7937, -0.3004, -0.8048, -1.0061, -1.0509, -1.9337, -1.2074,
       -1.0706,  0.6826, -0.1657, -1.0804,  1.0552, -0.6639,  1.1671,
        1.6211, -1.57  , -0.2482, -0.5175, -0.5989,  0.5554, -0.6229,
       -0.496 , -0.1681, -0.3734, -1.1967,  0.7707,  0.6671, -0.6991,
       -0.0088, -2.09  ,  1.7704, -0.3091,  0.8038,  0.6138,  1.3579,
       -0.4333,  0.2038,  0.5591,  0.8725,  1.1544, -0.4774, -0.6642,
        0.3295, -2.0371,  1.57  , -0.3023, -0.0046, -0.6823, -0.0482,
        1.2711,  0.7709,  0.4927,  0.0889, -1.4456, -0.8441, -0.3432,
        0.4577,  0.2827,  0.9835,  0.4736,  0.0544,  0.2783, -1.2327,
       -0.4319,  1.86  ,  1.2004,  1.8161, -0.1109,  0.9763, -1.4528,
        0.784 , -0.1577, -1.3551,  1.0326, -1.8101, -1.9127, -0.1668,
       -1.066 ,  0.8425, -0.7309, -0.3638, -0.6648,  1.1232,  1.7587,
        1.8274, -1.2818, -1.0752, -0.5634,  0.3703,  0.3093, -0.583 ,
       -0.6619, -0.9974, -2.6542, -0.4718,  0.282 , -1.4297, -0.6698,
        1.0354, -0.0726, -0.8499, -0.8087,  0.7208, -0.5178,  0.5109,
       -0.6268, -1.13  ])


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

