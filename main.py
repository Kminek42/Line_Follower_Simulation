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

genotype = np.array([-3.6800e-02, -2.7350e-01, -1.0153e+00, -1.2390e-01,  2.8108e+00,
        1.3190e-01, -1.5185e+00,  7.0980e-01,  2.1220e-01,  4.8160e-01,
       -1.1526e+00,  4.6420e-01,  1.0180e-01, -4.7690e-01, -6.5760e-01,
       -6.2880e-01, -9.7120e-01, -8.6740e-01,  6.8420e-01,  4.0050e-01,
        6.2040e-01,  4.8190e-01,  1.6571e+00,  1.1190e-01,  6.1870e-01,
       -6.6090e-01, -5.0270e-01, -2.3320e-01, -3.3010e-01,  5.3890e-01,
        9.6950e-01,  1.6490e-01,  1.4390e+00,  9.4390e-01,  4.2540e-01,
       -4.4210e-01, -3.1779e+00, -5.1730e-01, -1.0560e-01,  4.1840e-01,
        7.7400e-02,  5.5710e-01,  1.4951e+00,  3.3400e-01,  6.8860e-01,
       -5.0730e-01, -8.4660e-01,  7.2500e-02, -7.3470e-01, -6.9280e-01,
       -1.6410e+00, -3.9050e-01, -1.1500e+00, -9.0710e-01, -1.1127e+00,
       -2.5586e+00, -8.2650e-01,  4.7120e-01, -1.2374e+00, -1.3028e+00,
        1.1537e+00, -2.8000e-03, -9.3500e-02,  1.6588e+00,  1.0617e+00,
       -8.5100e-02, -6.7480e-01, -7.2030e-01, -7.1300e-02,  1.6670e-01,
        3.0650e-01,  8.7510e-01, -1.6620e-01, -3.6120e-01, -2.1092e+00,
       -1.0938e+00,  7.4000e-02,  1.0400e-02, -3.6430e-01,  1.5459e+00,
        8.1770e-01,  4.9040e-01,  1.2900e-02, -1.8550e-01, -5.5180e-01,
        4.3690e-01, -3.8960e-01,  1.9060e-01,  3.1560e-01,  5.4540e-01,
       -8.4900e-02, -1.0251e+00,  1.3100e-02, -2.3548e+00,  1.5527e+00,
       -2.3850e-01,  1.1741e+00, -1.3956e+00,  9.8350e-01,  6.7540e-01,
        5.8100e-01, -3.4900e-02,  6.9800e-01,  1.2134e+00,  6.4920e-01,
        5.3780e-01, -7.7000e-03,  1.1755e+00, -5.2250e-01, -3.0130e-01,
        7.6050e-01,  1.9282e+00,  7.2490e-01, -2.3010e-01,  1.4950e-01,
       -6.3850e-01,  3.0760e-01, -8.2500e-02, -6.8740e-01, -1.5079e+00,
        3.5070e-01,  8.8230e-01, -7.9100e-01, -5.9050e-01, -7.3600e-02,
        8.1100e-01, -4.0080e-01, -1.7380e-01,  7.3580e-01,  1.4575e+00,
        1.4297e+00,  1.0529e+00, -3.2610e-01,  1.0390e-01,  1.1870e+00,
       -5.1200e-02,  1.9300e-02,  1.2726e+00,  1.0690e+00,  1.9170e-01,
       -1.0505e+00, -3.2610e-01,  1.4820e+00, -3.6650e-01, -3.5930e-01,
        2.7849e+00, -9.1400e-02, -3.0480e-01,  1.4302e+00,  4.7200e-02,
        9.7000e-03,  1.0292e+00, -1.6335e+00,  4.2000e-03, -8.0950e-01,
        9.0090e-01, -6.9850e-01, -5.8160e-01,  3.9230e-01, -1.8834e+00,
        8.9950e-01, -1.2900e-02,  1.0309e+00, -1.9392e+00,  7.3400e-02,
        1.0466e+00, -4.4800e-02, -6.5640e-01,  1.0608e+00,  2.2650e-01])


c = robot_controller.RobotController4(genotype[:170])

N=1
r = robot.Robot(
        max_motor_speed=1.0,
        wheelbase=[0.2],
        lenght=[0.14],
        engine_cutoff=0.05,
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

