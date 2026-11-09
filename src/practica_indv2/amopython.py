import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt


delta = lambda x_initial, x_final : x_final - x_initial

data = np.loadtxt(
    Path(__file__).parent / "resources/path_SRA2526.txt",
    dtype=[("x", float), ("y", float), ("t", float)],
)
print(data['t'])

delta = lambda data : np.diff(data)
v = lambda points, time : delta(points) / delta(time)
x = data['x']
y = data['y']
t = data['t']


def get_lineal_velocity(data):

    delta_x = delta(x)
    delta_y = delta(y)
    delta_t = delta(t)

    return np.sqrt((delta_x**2 + delta_y**2))/delta_t


def get_angular_velocity(data):
    vx = v(x, t)
    vy = v(y, t)
    theta = np.unwrap(np.arctan2(vy, vx))
    return np.diff(theta) / np.diff(data['t'][1:]) 

plt.subplot(131)
plt.plot(data['x'], data['y'])
plt.scatter(data['x'][0], data['y'][0], color='red')
plt.subplot(132)
print(np.max(get_angular_velocity(data)))
plt.plot(data['t'][2:], get_angular_velocity(data))
plt.subplot(133)
plt.plot( data['t'][1:], get_lineal_velocity(data))
plt.show()


## Apartado B
# Velocidad Máxima con los T para poder graficarlo
np.argmax(data['x'])


# Velocidad media

# Valocidad mínima

# Aceleración Máxima con los T para poder graficarlo

# Aceleración media

# Aceleración Minima

# Puntos por los que se haya pasado +1 vez

# media de visitas por puntos para saber si repites muchas veces el mismo recorrido