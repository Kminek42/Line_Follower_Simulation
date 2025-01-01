from robot import Robot
from track import Track
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
track.add_segment("straight")
track.add_segment('smooth_left')
track.add_segment('straight')
track.add_segment('smooth_right')
track.add_segment("straight")
track.add_segment('90_left')
track.add_segment('90_right')
track.add_segment('90_right')
track.add_segment('90_left')
track.add_segment('x-intersection')

for _ in range(160):
    track.add_segment("")
track.finalize(128)

total_children = 1260
children_per_generation = 10
sim_time = 10
dt = 5e-3
progres = 0
network_shape = np.array([10, 7, 4])
genotypes = np.random.randn(children_per_generation, get_parameters_num(network_shape))
t0 = time()
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
        sensor_noise=0.0,
        sensor_radius=0.005,
        track_width=0.018
    )
    controller = RobotController(network_shape, genotypes, network_shape[0] - 8)
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
    progres += children_per_generation
    print(scores[0] / sim_time, progres)
    genotypes = genotypes[id]
    genotypes = reproduce2(genotypes, scores, children_per_generation, 1e-2, 1e-1)
    
t1 = time()

print(f'Training time: {np.round(t1 - t0, 2)} seconds')

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
    network_shape
):
    pass