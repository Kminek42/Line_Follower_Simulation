import robot
import track
from genetic import reproduce2, save_genotype
import numpy as np
from time import time
import matplotlib.pyplot as plt
import robot_controller

np.random.seed(1)
np.set_printoptions(suppress=True)

t = track.Track()
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

for _ in range(160):
    t.add_segment("")
t.finalize(128)
# plt.axis('equal')
# plt.plot(t.chain[:, 0], t.chain[:, 1])
# plt.show()

child_n = 64
mutation_rate = 1/200
min_distance = 0.1
Y_mutation = []
alpha = 1.001
best = 0

parents = np.random.randn(child_n, 298)
scores = np.random.rand(child_n, )
dt = 1/200
i = 0
sim_time = 10
best_scores = []
average_scores = []

mutation_rate_sceduler = lambda a, score: a / (score + a)

while 2137:
    t0 = time()
    i += 1
    
    # create new robots --------------------------------------------------------
    children = reproduce2(parents, scores, child_n, mutation_rate, min_distance)
    children = np.round(children, 4)
    robots = robot.Robot(
        number_of_robots=child_n,
        max_acceleration=20.0,
        max_speed=1.0,
        acceleration_coefficient=50.0,
        wheelbase=0.07,
        position=[0.0, 0.0],
        rotation=np.radians(90),
        sensor_positions=np.array([0.0825, 0]) + np.array(np.meshgrid(np.linspace(-0.027, 0.0, 3), np.linspace(0.02765, -0.02765, 8))).T.reshape(-1, 2),
        sensor_noise=0.1,
        sensor_radius=0.005,
        track_width=0.018
    )

    c = robot_controller.RobotController(np.array([26, 8, 6, 4]), children, 2)

    # simulation ---------------------------------------------------------------
    for _ in np.arange(0, sim_time, dt):
        readings = robots.get_sensors(t)
        controls = c.get_motors(readings)
        robots.move(controls, dt)
        robots.distance_traveled[robots.get_distance(t) > 0.2] = -np.inf
        robots.distance_traveled[robots.distance_traveled < 0] = -np.inf
        robots.distance_traveled[robots.rotation > np.deg2rad(210)] = -np.inf
        robots.distance_traveled[robots.rotation < np.deg2rad(-30)] = -np.inf
        
    robots.distance_traveled[robots.distance_traveled < 1e-3] = 1e-3
    
    # sort by score ------------------------------------------------------------
    criterion = robots.distance_traveled
    id = np.argsort(-criterion)
    parents = children[id]
    scores = robots.distance_traveled[id]

    # update mutation rate -----------------------------------------------------
    Y_mutation.append(mutation_rate)
    np.savetxt('../output-data/MutationRate.csv', Y_mutation)
    best = np.round(scores[0] / sim_time, 2)
    mutation_rate = mutation_rate_sceduler(1e-3, best)
    print(f"Generation: {i}\nLearn time: {np.round(time() - t0, 2)} s\nmutation rate: {np.round(mutation_rate, 4)}\nbest specimen's average speed: {best} m/s\nsim time: {sim_time}s\n")
    best_scores.append(scores[0] / sim_time)
    np.savetxt('../output-data/BestScore.csv', best_scores)
    average_scores.append(np.mean(scores) / sim_time)
    np.savetxt('../output-data/AverageScore.csv', average_scores)

    # increase simulation time for longer, more difficult to complete track ----
    if robots.distance_traveled[id[0]] / sim_time > 0.5 and sim_time < 20:
        sim_time += 1
    
    if scores[0] > best:
        best = scores[0]
        save_genotype(parents[0], '../output-data/genotype.txt')
