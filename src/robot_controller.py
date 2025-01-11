import neural_network as nn
import numpy as np

class RobotController:
    def __init__(self, layers: np.array, parameters: np.array, memory_size: int):
        assert layers[-1] == 2 + memory_size, "Output layer should have 2 + memory_size neurons (for L/R motors and memory)."
        self.input_size = layers[0]
        self.network = nn.NeuralNetwork(layers, parameters)
        self.memory = np.zeros([parameters.shape[0], memory_size])
        self.memory_size = memory_size
        
    def get_motors(self, sensor_readings):
        assert self.input_size == len(sensor_readings[0]) + self.memory_size, "Input layer should have sensor_readings + memory_size neurons."
        x = np.concatenate((sensor_readings, self.memory), axis=1)
        
        x = self.network.forward(x)
        
        self.memory = x[:, 2:]
        x = x[:, :2]
        
        return x
