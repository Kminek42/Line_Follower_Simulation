import simulation
from genetic import get_next_generation, save_genotype
import numpy as np
from time import time
import matplotlib.pyplot as plt

np.random.seed(0)

t = simulation.Track()
t.add_segment("straight")
for _ in range(60):
    t.add_segment("")

# plt.axis('equal')
# plt.plot(t.chain[:, 0], t.chain[:, 1])
# plt.show()

def test_gens(gens):
    r = simulation.Robot(max_motor_speed=1.0)

    c = simulation.RobotController4(gens)
    s = simulation.Simulation(c, r, t, 1/200)
    return s.get_score(15)

g1 = np.random.randn(170)
g2 = np.random.randn(170)

i = 0
while 2137:
    t0 = time()
    i += 1
    s1, g1, s2, g2 = get_next_generation(g1, g2, test_gens, 256, 1/16)
    print(f"Generation: {i}\nScore: {s1}, {s2}\n\n")
    if s1 > s2:
        save_genotype(g1, "genotype.txt")

    else:
        save_genotype(g2, "genotype.txt")

        
    print(f"Time: {time() - t0}")