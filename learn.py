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
    r = simulation.Robot()

    c = simulation.RobotController4(gens)
    s = simulation.Simulation(c, r, t, 1/200)
    return s.get_score(15)

g1 = np.array([-4.42552594e-01,  6.10529852e-01, -3.93364161e-01,  2.15590003e-01,
        3.34389285e-02, -5.49728283e-01, -1.56349669e+00, -8.75791078e-01,
        6.76177768e-01, -1.03686917e+00, -3.33057401e-01, -2.05808463e+00,
        1.46274045e+00,  1.53502913e+00,  9.12200808e-01,  6.93453103e-01,
        2.76355408e-02,  6.09459638e-02,  5.54495937e-01, -5.69517264e-01,
        1.41078282e+00, -4.62505539e-01,  2.32343562e-01,  6.39735995e-01,
        1.17329352e+00, -1.31998255e+00, -2.88346794e+00, -1.93320478e+00,
        2.48530627e-01,  1.03221141e+00, -1.39473962e-01, -1.90655979e-01,
        4.48637527e-01, -9.92429772e-01, -2.25939656e-01, -3.21826652e-01,
       -6.39722638e-01,  1.04655353e+00,  3.11363503e-01, -7.76020467e-01,
       -3.07364810e-01, -1.58143524e+00, -2.48198826e-01, -4.57922420e-01,
        4.25393398e-01, -3.08361251e-01,  1.42273213e+00,  1.01946139e+00,
       -8.96762977e-01, -9.56740516e-01, -1.32468484e+00, -7.40747471e-01,
       -6.75021832e-01,  1.33033173e+00,  6.19801063e-01,  6.76125558e-01,
       -3.26683154e-01,  7.48197522e-01,  5.46908067e-01, -8.58985321e-01,
       -4.80235332e-03,  4.88426467e-01, -8.38330966e-01,  3.81163744e-01,
       -9.90903282e-01,  6.29483419e-01,  7.63796155e-01, -8.86406268e-01,
        1.92134696e+00, -1.66949067e+00, -1.08903444e+00,  9.84117293e-01,
        9.16277201e-01, -4.36537093e-01,  1.94378760e+00,  7.13389571e-01,
       -7.28057719e-01,  8.39516458e-01, -1.08002186e+00, -1.78480389e+00,
       -7.96185839e-01, -1.40054127e+00, -1.84350577e-01,  5.01785477e-03,
       -6.54397262e-01,  8.06741891e-01,  6.97372824e-01, -2.67650554e-01,
        1.16807923e+00,  3.65651446e-01, -1.79213853e-01,  1.63989905e+00,
        3.10153058e+00,  4.88734744e-01, -1.15477553e+00, -1.94273744e-01,
       -2.82135142e-01, -9.75654666e-01,  9.81866908e-02,  9.05489953e-01,
       -1.47335474e+00, -1.14898854e-01,  1.74303872e+00, -2.63415723e-02,
        7.55909436e-01, -2.07317997e-01, -8.06642539e-01,  1.06424968e+00,
        1.59933656e+00, -7.72457707e-01, -1.29363428e+00, -6.91243975e-01,
       -1.21442965e+00, -4.85676173e-01, -5.16972371e-02,  5.67056372e-01,
        1.06783358e+00, -9.85448716e-01,  6.19301766e-01, -5.86259952e-02,
        1.25657140e+00,  3.49691113e-01,  3.98585727e-01,  8.62866895e-01,
       -8.35168139e-01, -1.48526881e-01, -1.57458215e+00, -2.67426661e-01,
       -1.17574793e-01,  1.43972367e-02,  4.79831965e-01,  2.68953815e-01,
       -4.46790199e-01, -2.26002068e-01, -4.40459020e-01, -1.35373284e+00,
        1.82452708e+00, -1.18616117e-01, -8.08116055e-01, -7.18910946e-01,
       -5.73543922e-01, -3.83677186e-01,  2.91634040e-01,  7.28569828e-02,
       -1.85542451e-02, -8.05092642e-01,  3.19791899e-01, -1.17636888e+00,
       -1.76965102e+00,  7.49491334e-05, -9.82699680e-01, -2.07067642e-01,
       -3.46339467e-01,  8.43518907e-01,  1.51063288e+00,  2.00012876e+00,
        5.46734365e-01, -2.10082473e+00,  1.00607292e+00,  4.81470807e-02,
       -1.80526763e+00, -1.10219609e+00,  1.76723461e-01, -9.49315383e-01,
       -1.24760574e+00, -1.01910926e+00,  7.55208981e-01,  3.45328205e-01,
       -1.45098437e-01, -1.04278632e-01])


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