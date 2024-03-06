import numpy as np
from matplotlib.pyplot import plot, show
import sys

data = np.loadtxt(sys.argv[1])
plot(data)
show()