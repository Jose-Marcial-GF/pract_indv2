import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt


delta = lambda x_initial, x_final : x_final - x_initial

data = np.loadtxt(
    Path(__file__).parent / "resources/path_SRA2526.txt",
    dtype=[("x", float), ("y", float), ("t", float)],
)
print(data['t'])


def get_lineal_velocity(data):

    delta_x = np.diff(data['x'])
    delta_y = np.diff(data['y'])
    delta_t = np.diff(data['t'])

    return np.sqrt((delta_x**2 + delta_y**2))/delta_t


print(np.where(get_lineal_velocity(data)==0))

#fig, ax = plt.subplots()
#ax.plot(data['t'][1:], get_lineal_velocity(data), color = 'orange')

v = get_lineal_velocity(data)


vx = np.diff(data['x'])/np.diff(data['t'])
vy = np.diff(data['y'])/np.diff(data['t'])

# vx = v*cos(alpha)
theta = np.unwrap(np.arctan2(vy, vx))
velocidad_angular = np.diff(theta) / np.diff(data['t'][1:]) 

plt.subplot(131)
plt.plot(data['x'], data['y'])
plt.scatter(data['x'][0], data['y'][0], color='red')
plt.subplot(132)
print(np.max(velocidad_angular))
plt.plot(data['t'][2:], velocidad_angular)
plt.subplot(133)
plt.plot( data['t'][1:], get_lineal_velocity(data))
plt.show()
