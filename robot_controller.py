import numpy as np

class RobotController:
    def __init__(self, genotype: np.array):
        '''
        genotype: all data needed to describe controller behaviour, stored as 1D array
        '''
        self.activation = np.tanh
        self.w = []
        self.genotype = genotype
        shape = np.array([10, 8, 6, 4])

        parameters_n = 0
        for i in range(len(shape) - 1):
            parameters_n += shape[i] * shape[i+1]
            parameters_n += shape[i+1]

        assert len(self.genotype) == parameters_n, f"genotype: {len(self.genotype)}, parameters: {parameters_n}"
            
        for i in range(len(shape) - 1):
            self.w.append(genotype[:shape[i] * shape[i+1]].reshape(shape[i], shape[i+1]))
            genotype = genotype[shape[i] * shape[i+1]:]

            self.w.append(genotype[:shape[i+1]])
            genotype = genotype[shape[i+1]:]

        self.last_in = np.zeros([8])
        self.mem = np.zeros([shape[0] - 8])
        
    def get_motors(self, inputs):
        # if max(inputs) > 0.25:
        #     self.last_in = inputs
        # else:
        #     inputs = self.last_in

        inputs = np.concatenate((inputs, self.mem))
        for i in range(0, len(self.w), 2):
            inputs = inputs @ self.w[i]
            inputs += self.w[i + 1]
            inputs = self.activation(inputs)

        self.mem = inputs[2:]
        return inputs[0], inputs[1]
        
    def __repr__(self):
        return f"genotype: {self.genotype}"
