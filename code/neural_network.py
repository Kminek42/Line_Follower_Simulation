import numpy as np

class NeuralNetwork:
    def __init__(self, layer_sizes: np.ndarray, parameters: np.ndarray):
        assert layer_sizes.ndim == 1, 'Layer sizes must be a 1D array.'
        parameters_num = self._get_parameters_num(layer_sizes)
        assert parameters.shape[1] == parameters_num, f'Parameters must have {parameters_num} parameters in second dimension.'
        
        self.layers = []
        for layer_num, _ in enumerate(layer_sizes[:-1]):
            input_size = layer_sizes[layer_num]
            output_size = layer_sizes[layer_num + 1]
            weights_n = input_size * output_size
            biases_n = output_size
            
            layer_parameters = parameters[:, :weights_n + biases_n]
            layer = LinearLayer(input_size, output_size, layer_parameters, 'tanh')
            
            parameters = parameters[:, weights_n + biases_n:]
            
            self.layers.append(layer)
        
    def _get_parameters_num(self, layer_sizes: np.ndarray) -> int:
        total_parameters = 0
        for layer_num, _ in enumerate(layer_sizes[:-1]):
            weights_n = layer_sizes[layer_num] * layer_sizes[layer_num + 1]
            biases_n = layer_sizes[layer_num + 1]
            total_parameters += weights_n + biases_n
    
        return total_parameters

    def forward(self, x: np.ndarray) -> np.ndarray:
        assert x.ndim == 2, 'Inputs must be a 2D array (batch_n, input_size).'
        for layer in self.layers:
            x = layer.forward(x)
        return x
    

class LinearLayer():
    def __init__(self, input_size: int, output_size: int, parameters: np.ndarray, activation: str):
        self.activation = self._get_activation(activation)
        assert parameters.ndim == 2, 'Parameters must be a 2D array (batch_n, parameters_n).'
        batch_n = parameters.shape[0]
        weights_n = input_size * output_size
        biases_n = output_size
        assert parameters.shape[1] == weights_n + biases_n, f'Parameters must have {weights_n + biases_n} parameters in second dimension.'
        self.weights = parameters[:, :weights_n].copy().reshape(batch_n, output_size, input_size)
        self.biases = parameters[:, weights_n:].copy().reshape(batch_n, output_size)
    
    def _get_activation(self, activation: str) -> callable:
        if activation == 'binary':
            return lambda x: np.where(x >= 0, 1, -1)
        elif activation == 'hard_clip':
            return lambda x: np.clip(x, -1, 1)
        elif activation == 'relu':
            return lambda x: np.maximum(0, x)
        elif activation == 'tanh':
            return lambda x: np.tanh(x)
        else:
            raise ValueError(f'Unsupported activation function: {activation}')
    
    def forward(self, x: np.ndarray) -> np.ndarray:
        assert x.ndim == 2, 'Inputs must be a 2D array (batch_n, input_size).'
        assert x.shape[0] == self.weights.shape[0], f'Batches size must match (input batch_n: {x.shape[0]}, linear batch_n: {self.weights.shape[0]}).'
        assert x.shape[1] == self.weights.shape[2], 'Input size must match the weight matrix.'

        return self.activation(np.einsum('bnm, bm -> bn', self.weights, x) + self.biases)
