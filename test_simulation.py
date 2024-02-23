import robot
import track
import numpy as np

r = robot.Robot(
    max_motor_speed=1.0,
    wheelbase=0.2,
    lenght=0.14,
    engine_cutoff=0.01)

r2 = robot.Robot2(
    max_motor_speed=1.0,
    wheelbase=0.2,
    lenght=0.14,
    engine_cutoff=0.01)


for _ in range(200):
    r.move(0.2, 0.7, 1/200)
    r2.move(0.2, 0.7, 1/200)

print(np.round(r.position, 3))
print(np.round(r2.position, 3))
print(sum(r.position - r2.position) / np.max(np.abs((r.position, r2.position))))

for _ in range(200):
    r.move(1.0, -0.2, 1/200)
    r2.move(1.0, -0.2, 1/200)

print(np.round(r.position, 3))
print(np.round(r2.position, 3))
print(sum(r.position - r2.position) / np.max(np.abs((r.position, r2.position))))
