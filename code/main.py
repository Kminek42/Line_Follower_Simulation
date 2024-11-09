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
genotype = np.array([-1.4727, -0.8043, -1.0702, -0.9254, -0.5788,  0.2129,  0.1506,
       -0.3436, -1.9861,  1.5484, -0.0703, -1.8422,  0.8262, -1.2229,
       -0.5382,  0.624 , -0.339 ,  0.2169,  1.3022,  0.0442, -0.2623,
       -2.0382, -0.3794, -1.2157, -0.9647,  1.5287,  1.2064, -0.7272,
       -0.2409, -1.5659,  0.4139,  0.7808,  0.2515,  1.2657,  1.9626,
        0.3021,  0.4935, -0.758 ,  1.9061, -1.013 ,  0.0302, -0.5895,
       -0.7197,  1.5974, -0.845 ,  0.0409,  0.1113,  0.9641,  0.7347,
        0.5188,  2.0095, -1.2322, -0.2278,  0.6355, -1.4287,  1.0688,
        0.1887, -0.9646, -0.9148, -0.8756, -0.1872, -1.1152,  0.0425,
        0.8383, -0.1823, -0.169 ,  0.7477,  1.2241, -0.2654, -0.7642,
        1.4955,  1.2516,  1.0672,  1.3636,  0.8619,  0.3625,  0.4661,
        0.9047, -0.7192,  0.0218,  0.0305, -2.5171, -0.5924, -1.4277,
       -1.0872, -1.255 ,  0.7034, -0.1932,  0.056 , -0.5804,  0.0866,
       -1.4079,  0.0488,  1.0369,  0.9986, -0.3962, -3.1522,  0.8787,
        0.4374, -0.4239,  0.4744,  0.3703, -0.6948, -0.3331, -0.0742,
        0.9258, -0.6196, -0.161 , -0.3776,  0.506 , -0.8311, -0.9755,
       -0.6714,  0.6725, -0.7334, -0.9678, -0.2896, -0.6181,  1.0407,
        2.1308, -0.3892, -0.4014,  0.1995, -1.7624,  1.724 , -0.3537,
        0.8558, -0.0034,  1.6288, -2.6173,  1.1871, -0.6355,  1.3609,
       -0.4297,  1.018 ,  0.6605, -0.8153, -1.4157, -2.1657,  1.6457,
        0.4295, -0.1482,  0.161 , -2.188 , -0.5532,  0.1554, -0.7093,
        1.359 , -2.4997,  1.1345, -0.1975,  0.8376,  0.0578, -0.1604,
       -0.4873,  0.0217, -1.8073,  0.1725,  1.0172, -2.724 , -2.2215,
        0.0145, -0.9713, -1.5307, -0.2636,  0.4757, -0.083 ,  1.743 ,
       -0.3373, -0.6909])


c = robot_controller.RobotController(np.array([10, 8, 6, 4]), genotype.reshape(1, -1), 2)

child_n=1
r = robot.Robot(
    number_of_robots=child_n,
    max_acceleration=20.0,
    max_speed=1.0,
    acceleration_coefficient=50.0,
    wheelbase=0.2,
    position=[0.0, 0.0],
    rotation=np.radians(90),
    sensor_positions=np.array([0.14, 0]) + np.array(np.meshgrid(np.linspace(0.0, 0.0, 1), np.linspace(0.033, -0.033, 8))).T.reshape(-1, 2),
    sensor_noise=0.1,
    sensor_radius=0.005,
    track_width=0.018
)

t = Track(tile_size=0.25)
t.add_segment("straight")
t.add_segment('smooth_left')
t.add_segment('straight')
t.add_segment('smooth_right')
t.add_segment("straight")
t.add_segment('90_left')
t.add_segment('90_right')
t.add_segment('90_right')
t.add_segment('90_left')
t.add_segment('x-intersection')
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

