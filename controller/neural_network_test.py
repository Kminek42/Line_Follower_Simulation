import neural_network as nn
import numpy as np

batch_n = 7
inputs_n = 3
hidden_n = 5
outputs_n = 2

parameters = np.random.randn(batch_n, 8)

layer = nn.LinearLayer(inputs_n, outputs_n, parameters, 'tanh')

x = np.random.randn(batch_n, inputs_n)

print(layer.forward(x))

parameters = np.random.randn(batch_n, 32)
layers = np.array([inputs_n, hidden_n, outputs_n])

neural_network = nn.NeuralNetwork(layers, parameters)

x = np.random.randn(batch_n, inputs_n)

print(neural_network.forward(x))
