from robot import Robot
from track import Track, SegmentType
from neural_network import get_parameters_num
from genetic import reproduce2, save_genotype
import numpy as np
from time import time
import matplotlib.pyplot as plt
from robot_controller import RobotController
import pandas as pd

np.random.seed(1)
np.set_printoptions(suppress=True)

track = Track()
track.add_segment(SegmentType.STRAIGHT)
track.add_segment(SegmentType.SMOOTH_LEFT)
track.add_segment(SegmentType.STRAIGHT)
track.add_segment(SegmentType.SMOOTH_RIGHT)
track.add_segment(SegmentType.STRAIGHT)
track.add_segment(SegmentType.LEFT_90)
track.add_segment(SegmentType.RIGHT_90)
track.add_segment(SegmentType.LEFT_90)
track.add_segment(SegmentType.RIGHT_90)
track.add_segment(SegmentType.X_INTERSECTION)

for _ in range(160):
    track.add_segment()
track.finalize(128)


def simulate(
    robots,
    track,
    controller, 
    sim_time,
    dt
):
    for _ in np.arange(0, sim_time, dt):
        readings = robots.get_sensors(track)
        controls = controller.get_motors(readings)
        robots.move(controls, dt)
        robots.distance_traveled[robots.get_distance(track) > 0.2] = -np.inf
        robots.distance_traveled[robots.distance_traveled < 0] = -np.inf
        robots.distance_traveled[robots.rotation > np.deg2rad(210)] = -np.inf
        robots.distance_traveled[robots.rotation < np.deg2rad(-30)] = -np.inf
    
    robots.distance_traveled[robots.distance_traveled < 0] = 0
    
    # sort by score ------------------------------------------------------------
    criterion = robots.distance_traveled
    id = np.argsort(-criterion)
    scores = robots.distance_traveled[id]
    
    return id, scores


def learn(
    total_children,
    children_per_generation,
    mutation_rate,
    network_shape,
    show_results=False
):
    progres = 0
    Y_scores = [0]
    X_running_children = [0]
    
    genotypes = np.random.randn(children_per_generation, get_parameters_num(network_shape))
    while progres < total_children:
        robots = Robot(
            number_of_robots=children_per_generation,
            max_acceleration=20.0,
            max_speed=1.0,
            acceleration_coefficient=100.0,
            wheelbase=0.2,
            position=[0.0, 0.0],
            rotation=np.radians(90),
            sensor_positions=np.array([0.14, 0]) + np.array(np.meshgrid(np.linspace(0.0, 0.0, 1), np.linspace(0.033, -0.033, 8))).T.reshape(-1, 2),
            sensor_noise=0.1,
            sensor_radius=0.005,
            track_width=0.018
        )
        controller = RobotController(network_shape, genotypes, network_shape[0] - 8)

        id, scores = simulate(robots, track, controller, sim_time, 5e-3)
        progres += children_per_generation
        avg_speed = scores[0] / sim_time
        genotypes = genotypes[id]
        genotypes = reproduce2(genotypes, scores, children_per_generation, mutation_rate, 1e-1)
        if show_results:
            print(avg_speed)
        Y_scores.append(avg_speed)
        X_running_children.append(progres)
        
    X_interp = np.arange(0, total_children + 1, 10)
    Y_scores = np.interp(X_interp, np.array(X_running_children), np.array(Y_scores))
    return X_interp, Y_scores, genotypes


total_children = 5000
sub_learns = 100
sim_time = 10
dt = 5e-3

# _, _, genotypes = learn(1280*4, 30, 0.01, np.array([10, 7, 4]), True)
# np.savetxt('genotype.csv', genotypes[0].reshape(1, -1), delimiter=',')
# print(genotypes[0])
# exit()



# children_per_genration_array = [8, 30, 60]
# mutation_rate_array = [1e-1, 1e-2, 1e-3]
# network_size_array = [[10, 7, 4]]

children_per_genration_array = [30]
mutation_rate_array = [1e-2]
network_size_array = [[8, 2], [8, 5, 2], [10, 4], [10, 7, 4], [10, 8, 6, 4]]
network_size_array = [[9, 3, 3]]

total_steps = len(children_per_genration_array) * len(mutation_rate_array) * len(network_size_array) * sub_learns

results = {}

current_steps = 0
t0 = time()

for children_per_generation in children_per_genration_array:
    for mutation_rate in mutation_rate_array:
        for network_size in network_size_array:
            Y_temp = (0 * np.arange(0, total_children + 1, 10)).astype(np.float32)
            c = f'C={children_per_generation}, M={mutation_rate}, N={repr(network_size)}'
            print(c)
            best_score = 0
            best_y = 0
            for run in range(sub_learns):
                X, Y, genotypes = learn(total_children, children_per_generation, mutation_rate, np.array(network_size))
                temp_score = Y[-1]
                if temp_score > best_score:
                    best_score = temp_score
                    print(best_score)
                    best_y = Y
                    np.savetxt(f'data/results/learning_results {c}.csv', Y)
                    np.savetxt(f'data/genotypes/genotype {c}.csv', genotypes[0].reshape(1, -1), delimiter=',')
                
                current_steps += 1
                t1 = time()
                learning_time = t1 - t0
                estimated_remaining_time = learning_time * total_steps / current_steps - learning_time
                print(f'Learning time: {np.round(learning_time, 2)}s, remaininng time: {np.round(estimated_remaining_time, 2)}s')
                
            
            
            
            
