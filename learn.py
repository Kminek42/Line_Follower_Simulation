import robot
import track
import robot_controller
from genetic import reproduce2, save_genotype
import numpy as np
from time import time
import matplotlib.pyplot as plt

t = track.Track()
t.add_segment("straight")
t.add_segment('90_left')
t.add_segment('straight')
t.add_segment('90_right')
t.add_segment("straight")
t.add_segment('90_left')
t.add_segment('straight')
t.add_segment('90_right')

for _ in range(160):
    t.add_segment("")
t.finalize(128)
# plt.axis('equal')
# plt.plot(t.chain[:, 0], t.chain[:, 1])
# plt.show()

child_n = 256
mutation_rate = 1/128
parents = np.random.randn(child_n, 170)
scores = np.random.rand(child_n, )
dt = 1/200
i = 0
sim_time = 20
Y = []
while 2137:
    t0 = time()
    i += 1
    
    children = reproduce2(parents, scores, child_n, mutation_rate)
    children = np.round(children, 10)
    robots = robot.Robot(
        max_motor_speed=1.0,
        wheelbase=[0.2] * child_n,
        lenght=[0.14] * child_n,
        engine_cutoff=0.05,
        rotation=np.pi/2,
        sensor_width=[0.067] * child_n,
        sensor_n=8,
        sensor_noise=0.1,
        sensor_radius=0.005,
        min_speed=0.1,
        position=[0.0, 0.0],
        track_width=0.02
    )

    # c = [robot_controller.RobotController4(child) for child in children[:, :170]]
    c = robot_controller.RobotController4_batch(children[:, :170])

    for _ in np.arange(0, sim_time, dt):
        readings = robots.get_sensors(t)
        controls = c.get_motors(readings)
        robots.move(controls[0], controls[1], dt)
        robots.mileage[robots.get_distance(t) > 0.2] = -np.inf
        robots.mileage[robots.mileage < 0] = -np.inf
        robots.mileage[robots.rotation > np.deg2rad(225)] = -np.inf
        robots.mileage[robots.rotation < np.deg2rad(-45)] = -np.inf
        
    id = np.argsort(-robots.mileage)
    parents = children[id]
    scores = robots.mileage[id]
    print(f"Generation: {i}, Learn time: {np.round(time() - t0, 2)} s, best specimen's average speed: {np.round(scores[0] / sim_time, 2)} m/s, sim time: {sim_time}s")

    if robots.mileage[id[0]] / sim_time > 0.7 and sim_time < 20:
        sim_time += 1
    
    Y.append(robots.mileage[id[0]] / sim_time)
    np.savetxt('Evolution.csv', Y)
    save_genotype(parents[0], 'genotype.txt')

    print()



t0 = time()
i += 1

