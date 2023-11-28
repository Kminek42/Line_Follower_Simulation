from track import Track
import numpy as np
import robot
from time import time

def model(inputs, weights):
    return inputs @ weights

best_w = 0
best_d = 0

# robot and track initialization
r = robot.Robot(max_motor_speed=1, lenght=0.15, wheelbase=0.2, sensor_n=8, sensor_width=0.07)

t = Track()
t.add_segment("straight")
for i in range(20):
    t.add_segment("")

weights = np.array(
[[-0.14901069,  0.44030038],
         [ 0.24909627,  0.02049112],
         [ 0.07700896,  0.7889302 ],
         [ 0.6718489 , -0.38360402],
         [ 0.3624823 , -0.351407  ],
         [ 0.590201  ,  0.10290837],
         [-0.46667278, -0.40737876],
         [-0.06750615,  0.19017002]])

# simulation ---------------------------------------------------------------
t0 = time()
for n in range(10):
    r = robot.Robot(max_motor_speed=1, lenght=0.15, wheelbase=0.2, sensor_n=8, sensor_width=0.07)
    t = Track()
    t.add_segment("straight")
    for i in range(20):
        t.add_segment("")

    for i in range(100):
        inputs = np.array(r.get_sensors(t))
        # inputs = np.random.randn(8)
        outputs = inputs @ weights
        e1 = outputs[0]
        e2 = outputs[1]
        r.move(e1, e2, 0.01)

print((time() - t0) / 10)
