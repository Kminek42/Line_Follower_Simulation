from track import Track
import numpy as np
import robot
from time import time

class Network:
    def __init__(self, weights: np.array, shape):
        self.last = np.zeros([8])
        self.w = []
        self.genotype = weights
        self.shape = shape

        # assert shape[0] == shape[-1] + 6, f"Inputs: {shape[0]}, Outputs + 6: {shape[-1] + 6}"

        parameters_n = 0
        for i in range(len(shape) - 1):
            parameters_n += shape[i] * shape[i+1]
            parameters_n += shape[i+1]

        assert len(self.genotype) == parameters_n, f"genotype: {len(self.genotype)}, parameters: {parameters_n}"
            
        
        for i in range(len(shape) - 1):
            self.w.append(weights[:shape[i] * shape[i+1]].reshape(shape[i], shape[i+1]))
            weights = weights[shape[i] * shape[i+1]:]

            self.w.append(weights[:shape[i+1]])
            weights = weights[shape[i+1]:]

    def forward(self, inputs):
        if max(inputs) > 0.25:
            self.last = inputs
        else:
            inputs = self.last

        output_r = inputs
        for i in range(0, len(self.w), 2):
            output_r = output_r @ self.w[i]
            output_r += self.w[i + 1]
            output_r = np.arctan(output_r)
        
        output_r = output_r[0]

        output_l = inputs[::-1]
        for i in range(0, len(self.w), 2):
            output_l = output_l @ self.w[i]
            output_l += self.w[i + 1]
            output_l = np.arctan(output_l)

        output_l = output_l[0]

        return output_l, output_r
    
    def __repr__(self):
        return f"genotype: {self.genotype}\nshape: {self.shape}"

class Problem:
    def __init__(self):
        self.track = Track()
        self.track.add_segment("straight")
        for i in range(40):
            self.track.add_segment("")

    def get_score(self, network: Network):
        self.robot = robot.Robot(max_motor_speed=1, lenght=0.15, wheelbase=0.2, sensor_n=8, sensor_width=0.07)
    
        s = 0
        for i in range(1000):
            inputs = np.array(self.robot.get_sensors(self.track))
            e1, e2 = network.forward(inputs)
            s += self.robot.move(e1, e2, 1/100)
            if self.track.distance_to_chain(self.robot.position[0], self.robot.position[1]) > 0.19:
                return -np.inf

            if self.robot.rotation > 170 or self.robot.rotation < -170:
                return -np.inf


        return s

def save_genotype(net: Network, filename):
    file = open(filename, "w")
    file.write(f"genotype = np.{repr(net.genotype)}\n\n")
    file.close()

def swap_elements(arr):
    num_swaps = np.random.randint(0, 3)  # Number of swaps
    for _ in range(num_swaps):
        idx1, idx2 = np.random.choice(len(arr), 2, replace=False)  # Randomly choosing 2 distinct indices
        arr[idx1], arr[idx2] = arr[idx2], arr[idx1]  # Swapping the elements at the chosen indices

    return arr

def crossover(gens1, gens2):
    if len(gens1) != len(gens2):
        raise ValueError("Arrays must be of the same length")

    crossover_point = np.random.randint(1, len(gens1) - 1)

    if np.random.randint(0, 2) == 0:
        genotype = np.concatenate((gens1[:crossover_point], gens2[crossover_point:]))
    
    else:
        genotype = np.concatenate((gens2[:crossover_point], gens1[crossover_point:]))

    return genotype

def mutate(genotype, mutation_rate):
    mask = np.random.rand(len(genotype)) < mutation_rate
    genotype[mask] = np.random.randn(np.count_nonzero(mask))
    return genotype

def learn_generation(parent1: Network, parent2: Network, children_n: int, p: Problem, mutation_rate=1e-2):
    children = [parent1, parent2]
    top = [0, parent1, 0, parent2]

    for i in range(children_n - 2):
        new_gens = crossover(parent1.genotype, parent2.genotype)
        mutate(new_gens, mutation_rate)
        children.append(Network(new_gens, parent1.shape))

    for child in children:
        score = p.get_score(child)

        worst_top = 2
        if top[0] < top[2]:
            worst_top = 0

        if score > top[worst_top]:
            top[worst_top] = score
            top[worst_top + 1] = child

    return top


l = False

if l:
    net1 = Network(np.random.randn(9), [8, 1])
    net2 = Network(np.random.randn(9), [8, 1])

    p = Problem()
    s1, p1, s2, p2 = learn_generation(net1, net2, 64, p)

    i = 0
    while 2137:
        i += 1
        s1, p1, s2, p2 = learn_generation(p1, p2, 64, p, 1e-1)
        print(f"Generation: {i}\nScore: {s1}, {s2}\n\n")
        if s1 > s2:
            save_genotype(p1, "genotype.txt")

        else:
            save_genotype(p2, "genotype.txt")

