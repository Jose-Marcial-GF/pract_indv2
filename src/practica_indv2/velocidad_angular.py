import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from practica_indv2.amopython import get_lineal_velocity

data = np.loadtxt(
    Path(__file__).parent / "resources/path_SRA2526.txt",
    dtype=[("x", float), ("y", float), ("t", float)],
)



v = get_lineal_velocity(data)


vx = np.diff(data['x'])/np.diff(data['t'])

# vx = v*cos(alpha)
alpha = np.arccos(vx/v)
plt.subplot(1, 2, 0)
plt.subplot(1, 2, alpha)

print(alpha)

