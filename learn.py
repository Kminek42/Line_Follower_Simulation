import robot
import track
import robot_controller
from genetic import reproduce, save_genotype
import numpy as np
from time import time
import matplotlib.pyplot as plt

np.random.seed(0)

t = track.Track()
t.add_segment("straight")
t.add_segment('90_left')
t.add_segment('straight')
t.add_segment('90_right')
for _ in range(80):
    t.add_segment("")
t.finalize(128)
# plt.axis('equal')
# plt.plot(t.chain[:, 0], t.chain[:, 1])
# plt.show()

N = 173
parent1 = np.random.randn(N)
parent2 = np.random.randn(N)
dt = 1/200
i = 0
sim_time = 4
while 2137:
    t0 = time()
    i += 1
    
    children = reproduce(parent1, parent2, N, N**-0.5)
    robots = robot.Robot(
        max_motor_speed=1.0,
        wheelbase=0.2 + 0.0 * children[:, 170],
        lenght=0.14 + 0.0 * children[:, 171],
        engine_cutoff=0.1,
        rotation=np.pi/2,
        sensor_width=0.067 + 0.0 * children[:, 172],
        sensor_n=8,
        sensor_noise=0.1,
        sensor_radius=0.005,
        min_speed=0.1,
        position=[0.0, 0.0],
        track_width=0.02
    )

    c = [robot_controller.RobotController4(child) for child in children[:, :170]]

    for _ in np.arange(0, sim_time, dt):
        readings = robots.get_sensors(t)
        controls = np.array([c[i].get_motors(readings[i]) for i in range(len(c))]).T
        robots.move(controls[0], controls[1], dt)
        robots.mileage[robots.get_distance(t) > 0.3] = -np.inf
        robots.mileage[robots.mileage < 0] = -np.inf
        robots.mileage[robots.rotation > np.deg2rad(225)] = -np.inf
        robots.mileage[robots.rotation < np.deg2rad(-45)] = -np.inf
        
    best_id = np.argsort(robots.mileage)[-2:]
    parent1, parent2 = children[best_id]
    print(f"Generation: {i}, Learn time: {np.round(time() - t0, 2)} s, best specimen's average speed: {np.round(robots.mileage[best_id[-1]] / sim_time, 2)} m/s, sim time: {sim_time}s")

    if robots.mileage[best_id[-1]] / sim_time > 0.7 and sim_time < 20:
        sim_time += 1
    
    save_genotype(parent2, 'genotype.txt')

    print()



t0 = time()
i += 1

