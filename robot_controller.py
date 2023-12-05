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


class RobotController2:
    def __init__(self, genotype: np.array):
        self.w = genotype[:8].T
        self.b = genotype[8]
        
    def get_motors(self, inputs):
        if max(inputs) > 0.25:
            self.last_in = inputs
        else:
            inputs = self.last_in

        l = inputs @ self.w + self.b
        r = inputs[::-1] @ self.w + self.b
        return l, r
        
    def __repr__(self):
        return f"genotype: {self.genotype}"


class RobotController3:
    def __init__(self):
        self.w = np.linspace(-0.27124883, 0.69846197, 8)
        self.scanning = True
        self.track = []
        self.steer_angle = 0
        self.steer_cutoff = 1e-1
        
    def set_mode(self, is_scanning: bool):
        self.scanning = is_scanning
        if (is_scanning):
            self.track = []

    def get_motors(self, inputs):
        if max(inputs) > 0.25:
            self.last_in = inputs
        else:
            inputs = self.last_in

        l = inputs @ self.w
        r = inputs[::-1] @ self.w
        if self.scanning:
            l = np.min([l, 0.5])
            r = np.min([r, 0.5])
            s_a = l - r
            self.steer_angle += self.steer_cutoff * (s_a - self.steer_angle)
            print(self.steer_angle)
        
        return l, r
        
    def __repr__(self):
        return f"genotype: {self.genotype}"