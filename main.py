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

genotype = np.array([ 0.09517287,  0.77586214,  1.11878178,  0.53167585, -0.7026687 ,
       -0.74410369,  0.44386097,  0.64911247,  1.06085053,  0.27442998,
        0.02459008, -0.40602452,  1.46274045,  1.16447535, -0.73835736,
        1.21461597,  0.10922339,  1.74179489, -0.31264513, -0.36523979,
       -0.64338046,  0.03312201,  0.80508258, -0.68381367, -0.91433864,
       -0.25753123, -2.88346794, -2.20723182, -0.12747591, -0.16263887,
       -0.48430735, -0.02873509,  0.44863753, -0.30921042,  0.85781399,
       -0.46232902,  1.06019049, -1.08058631,  0.34365989, -0.77602047,
        0.15377121, -1.58143524, -0.63214178, -0.56136005, -0.06738965,
       -0.30836125,  0.24030364,  1.01946139, -1.49376218,  0.88134133,
       -1.32468484, -0.22643626,  0.83728724,  1.69889172, -0.26546109,
        0.58050844, -0.31925732, -0.21950271,  0.54687476, -0.85898532,
       -0.93784238,  0.71238744, -0.83833097, -1.30521581,  0.09986955,
       -0.65314381, -2.26222846, -0.88640627,  0.21167394, -0.25552125,
       -1.08903444,  2.36728073,  0.88264231,  0.20728277, -0.53900815,
        0.93989698,  0.606389  ,  0.99510729,  1.39670637,  0.41216877,
       -0.24107359, -1.13702227,  1.03081595, -1.27698899,  0.83771977,
        0.93049765, -1.71384849,  0.07721229,  0.60457228, -0.48206776,
       -0.26658305,  2.69458733,  1.29137792, -0.33887665,  1.18566471,
       -0.15880047, -0.75483462, -1.99077882,  0.08973073,  0.11485388,
        0.79864258,  0.29877204, -0.35547902,  0.28922946,  0.38895685,
        0.94058319,  1.04105939,  0.16537621, -0.56059965,  0.40814812,
       -1.94071568,  1.07981324,  0.55926354, -0.81520184,  0.97546488,
       -0.36408678,  0.49225571, -1.30867214, -0.1202417 , -1.29105846,
       -0.8661071 , -0.37178976,  1.50124771, -2.57117597,  1.19732198,
       -0.48551504,  1.58844485, -0.46649941,  0.27580182, -1.54005989,
        0.1661819 , -1.6210875 , -2.2197708 , -0.38225815,  0.08208076,
        1.47504261, -0.35609911, -0.63117522, -0.40690255,  1.49072192,
       -1.05114711,  0.67763457,  1.81235465, -2.29413748,  0.65120935,
       -1.13049645, -0.89343989, -0.12461036,  1.33945302, -1.76743365,
        1.47879655,  2.42549196,  0.12864983,  2.23677301,  1.20472139,
        0.44126709, -0.43058327,  0.26166848, -0.806867  ,  0.85823779,
        0.25998028, -1.48590386, -1.90058426, -1.1375792 ,  0.23294444,
       -0.28862322,  1.04798222,  0.24995754,  0.04690446, -1.03224304])


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
