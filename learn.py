from track import Track
import numpy as np
import robot
from time import time

class Network:
    def __init__(self, w1, w2, b1, b2):
        if w1.shape[1] != b1.shape[0]:
            print(f"Error, w1 shape: {w1.shape[1]}, b1 shape: {b1.shape[0]}")
            exit()

        
        if w2.shape[0] != b1.shape[0]:
            print(f"Error, w2 shape: {w2.shape[0]}, b1 shape: {b1.shape[0]}")
            exit()

        if w2.shape[1] != b2.shape[0]:
            print(f"Error, w2 shape: {w2.shape[1]}, b1 shape: {b2.shape[0]}")
            exit()
        
        if w1.shape[0] != b2.shape[0] + 6:
            print(f"Error, w1 shape: {w1.shape[0]}, b2 shape: {b2.shape[0]} [difference should be 6]")
            exit()
        
        self.w1 = w1
        self.w2 = w2
        self.b1 = b1
        self.b2 = b2

        mem_N = b2.shape[0] - 2
        self.mem = np.zeros(mem_N)

    def forward(self, inputs):
        inputs = np.concatenate((inputs, self.mem))
        inputs = inputs @ self.w1
        inputs = inputs + self.b1
        inputs = np.arctan(inputs)

        inputs = inputs @ self.w2
        inputs = inputs + self.b2
        inputs = np.arctan(inputs)

        self.mem = inputs[2:]
        
        inputs = inputs[:2]
        return inputs[0], inputs[1]


class Problem:
    def __init__(self):
        self.track = Track()
        self.track.add_segment("straight")
        self.track.add_segment("90_left")
        self.track.add_segment("straight")
        self.track.add_segment("x-intersection")
        self.track.add_segment("straight")
        self.track.add_segment("90_right")
        self.track.add_segment("straight")
        for i in range(35):
            self.track.add_segment("")

    def get_score(self, network: Network):
        self.robot = robot.Robot(max_motor_speed=1, lenght=0.15, wheelbase=0.2, sensor_n=8, sensor_width=0.07)
    
        s = 0
        for i in range(1000):
            inputs = np.array(self.robot.get_sensors(self.track))
            e1, e2 = network.forward(inputs)
            s += self.robot.move(e1, e2, 1/100)
            if self.track.distance_to_chain(self.robot.position[0], self.robot.position[1]) > 0.09:
                return -np.inf

            if self.robot.rotation > 170 or self.robot.rotation < -170:
                return -np.inf


        return s
        
def swap_elements(arr):
    num_swaps = np.random.randint(0, 3)  # Number of swaps
    for _ in range(num_swaps):
        idx1, idx2 = np.random.choice(len(arr), 2, replace=False)  # Randomly choosing 2 distinct indices
        arr[idx1], arr[idx2] = arr[idx2], arr[idx1]  # Swapping the elements at the chosen indices

    return arr

l = True

if l:
    best_score = 0

    while 2137:
        w1 = np.random.randn(9, 4)
        w2 = np.random.randn(4, 3)
        b1 = np.random.randn(4)
        b2 = np.random.randn(3)

        net = Network(w1, w2, b1, b2)
        p = Problem()
        score = p.get_score(net)
        
        if score > best_score:
            print(score)
            best_score = score

            file = open("model.txt", "w")
            file.write(f"w1 = np.{repr(w1)}\n\n")
            file.write(f"w2 = np.{repr(w2)}\n\n")
            file.write(f"b1 = np.{repr(b1)}\n\n")
            file.write(f"b2 = np.{repr(b2)}\n\n")
            file.close()
