import robot
import track
import robot_controller
from genetic import reproduce2, save_genotype
import numpy as np
from time import time
import matplotlib.pyplot as plt

np.random.seed(42)
np.set_printoptions(suppress=True)

t = track.Track()
t.add_segment("straight")
t.add_segment('90_left')
t.add_segment('straight')
t.add_segment('90_right')
t.add_segment("straight")
t.add_segment('90_left')
t.add_segment('90_right')
t.add_segment('90_left')

for _ in range(160):
    t.add_segment("")
t.finalize(128)
# plt.axis('equal')
# plt.plot(t.chain[:, 0], t.chain[:, 1])
# plt.show()

child_n = 64
mutation_rate = 1/100
min_distance = 0.1
Y_mutation = []
steps = 1
alpha = 1.01
best = 0
current_steps = 0

parents = np.random.randn(child_n, 170)
scores = np.random.rand(child_n, )
dt = 1/200
i = 0
sim_time = 10
Y = []
while 2137:
    t0 = time()
    i += 1
    
    # create new robots --------------------------------------------------------
    children = reproduce2(parents, scores, child_n, mutation_rate, min_distance)
    children = np.round(children, 4)
    robots = robot.Robot(
        max_motor_speed=1.0,
        wheelbase=[0.2] * child_n,
        lenght=[0.14] * child_n,
        engine_acceleration=10.0,
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

    # simulation ---------------------------------------------------------------
    for _ in np.arange(0, sim_time, dt):
        readings = robots.get_sensors(t)
        controls = c.get_motors(readings)
        robots.move(controls[0], controls[1], dt)
        robots.mileage[robots.get_distance(t) > 0.2] = -np.inf
        robots.mileage[robots.mileage < 0] = -np.inf
        robots.mileage[robots.rotation > np.deg2rad(210)] = -np.inf
        robots.mileage[robots.rotation < np.deg2rad(-30)] = -np.inf
        
    # sort by score ------------------------------------------------------------
    id = np.argsort(-robots.mileage)
    parents = children[id]
    scores = robots.mileage[id]

    # update mutation rate -----------------------------------------------------
    Y_mutation.append(mutation_rate)
    np.savetxt('MutationRate.csv', Y_mutation)
    if np.round(scores[0] / sim_time, 2) > best:
        best = np.round(scores[0] / sim_time, 2)
        current_steps = 0
    else:
        current_steps += 1
        if current_steps == steps:
            mutation_rate *= alpha
    
    print(f"Generation: {i}, Learn time: {np.round(time() - t0, 2)} s, mutation rate: {mutation_rate}, best specimen's average speed: {np.round(scores[0] / sim_time, 2)} m/s, sim time: {sim_time}s")

    Y.append(robots.mileage[id[0]] / sim_time)
    np.savetxt('BestScore.csv', Y)

    # increase simulation time for longer, more difficult to complete track ----
    if robots.mileage[id[0]] / sim_time > 0.7 and sim_time < 20:
        sim_time += 1
    
    save_genotype(parents[0], 'genotype.txt')
