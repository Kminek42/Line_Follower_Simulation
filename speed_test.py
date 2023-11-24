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


for n in range(50):
    # creating random weights for next robot
    weights = np.random.uniform(-1, 1, (8,2))
    travelled_distance = 0

    # simulation ---------------------------------------------------------------
    for i in range(1000):
        inputs = np.array(r.get_sensors(t))
        outputs = inputs @ weights
        e1 = outputs[0]
        e2 = outputs[1]
        travelled_distance += r.move(e1, e2, 1/100)
    # --------------------------------------------------------------------------

    # update best robot weights
    print(travelled_distance)
    if best_d < travelled_distance:
        best_d = travelled_distance
        best_w = weights
        print(best_d, best_w)

    print(n)
