import numpy as np

class RobotController:
    def __init__(self, genotype: np.array):
        '''
        genotype: all data needed to describe controller behaviour, stored as 1D array
        '''
        self.activation = np.tanh
        self.w = []
        self.genotype = genotype
        shape = np.array([10, 7, 4])

        parameters_n = 0
        for i in range(len(shape) - 1):
            parameters_n += shape[i] * shape[i+1]
            parameters_n += shape[i+1]

        assert len(self.genotype) == parameters_n, f"genotype: {len(self.genotype)}, parameters: {parameters_n}"
            
        for i in range(len(shape) - 1):
            self.w.append(genotype[:shape[i] * shape[i+1]].reshape(shape[i + 1], shape[i]))
            genotype = genotype[shape[i] * shape[i+1]:]

            self.w.append(genotype[:shape[i+1]])
            self.w[-1] = self.w[-1].reshape(shape[i+1], 1)
            genotype = genotype[shape[i+1]:]

        self.last_in = np.zeros([8])
        self.mem = np.zeros([shape[0] - 8])
        self
        
    def get_motors(self, inputs):
        # if max(inputs) > 0.25:
        #     self.last_in = inputs
        # else:
        #     inputs = self.last_in
        
        inputs = inputs.reshape(1, -1).T
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
        # self.w = np.linspace(genotype[0], genotype[1], 8)
        self.b = genotype[8]
        
    def get_motors(self, inputs):
        if max(inputs) > 0.25:
            self.last_in = inputs

        inputs = self.last_in
        l = np.tanh(inputs @ self.w + self.b)
        r = np.tanh(inputs[::-1] @ self.w + self.b)
        return l, r
        
    def __repr__(self):
        return f"genotype: {self.genotype}"


class RobotController3:
    def __init__(self, genotype: np.array):
        self.w = genotype[:8].T
        # self.w = np.linspace(genotype[0], genotype[1], 8)
        self.b = genotype[8]

        self.mode = "normal"
        self.last_direction = ""
        self.direction_counter = 0

    def get_motors(self, inputs):
        # CurveSync ------------------------------------------------------------
        if max(inputs) > 0.25:
            self.last_in = inputs

        inputs = self.last_in
        l = np.tanh(inputs @ self.w + self.b)
        r = np.tanh(inputs[::-1] @ self.w + self.b)

        # PathPulse ------------------------------------------------------------
        steer_angle = l - r
        if steer_angle > 0.5:
            if self.last_direction != "right":
                self.last_direction = "right"
                self.direction_counter = 0
                print("right")
            
        elif steer_angle < -0.5:
            if self.last_direction != "left":
                self.last_direction = "left"
                self.direction_counter = 0
                print("left")

        else:
            self.direction_counter += 1
            if self.direction_counter > 256 and self.last_direction != "straight":
                self.last_direction = "straight"
                print("straight")
            
        return l, r
        
    def __repr__(self):
        return f"genotype: {self.genotype}"
    

class NeuralNetwok:
    def __init__(self, shape: np.array, genotype: np.array):
        self.activation = np.tanh
        self.w = []
        self.genotype = genotype


        parameters_n = 0
        for i in range(len(shape) - 1):
            parameters_n += shape[i] * shape[i+1]
            parameters_n += shape[i+1]

        assert len(self.genotype) == parameters_n, f"genotype: {len(self.genotype)}, parameters: {parameters_n}"
            
        for i in range(len(shape) - 1):
            self.w.append(genotype[:shape[i] * shape[i+1]].reshape(shape[i + 1], shape[i]))
            genotype = genotype[shape[i] * shape[i+1]:]

            self.w.append(genotype[:shape[i+1]])
            self.w[-1] = self.w[-1].reshape(shape[i+1], 1)
            genotype = genotype[shape[i+1]:]

        
    def forward(self, inputs):
        inputs = inputs.reshape(1, -1).T
        for i in range(0, len(self.w), 2):
            inputs = self.w[i] @ inputs
            inputs += self.w[i + 1]
            inputs = self.activation(inputs)
        
        inputs = np.clip(inputs, -1, 1)
        return inputs.T[0]
    
class RobotController4:
    def __init__(self, genotype: np.array):
        '''
        genotype: all data needed to describe controller behaviour, stored as 1D array
        '''
        self.nn = NeuralNetwok(np.array([10, 8, 6, 4]), genotype)

        self.mem = np.zeros(2)
        
    def get_motors(self, inputs):
        inputs = np.concatenate((inputs, self.mem))
        inputs = self.nn.forward(inputs)
        self.mem = inputs[2:]
        return inputs[0], inputs[1]
        
    def __repr__(self):
        return f"genotype: {self.genotype}"
