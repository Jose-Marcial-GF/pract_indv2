import numpy as np
from pathlib import Path



delta = lambda data : np.diff(data)
derivar = lambda points, time : delta(points) / delta(time)
data = np.loadtxt(
    Path(__file__).parent / "resources/path_SRA2526.txt",
    dtype=[("x", float), ("y", float), ("t", float)],
)
global x, y, t
x = data['x']
y = data['y']
t = data['t']


## Apartado A
def lineal_velocity():
    return np.hypot(delta(x), delta(y))/delta(t)

theta = np.unwrap(np.arctan2(derivar(y, t), derivar(x, t)))
def angular_velocity():
    theta = np.unwrap(np.arctan2(derivar(y, t), derivar(x, t)))
    return np.diff(theta) / np.diff(t[1:])


## Apartado B
# Periodicidad de las medidas de tiempo
dt = delta(t)


# Distancia recorrida, duración y desplazamiento neto
step = np.hypot(delta(x), delta(y))

# Distancia recorrida
total_distance = step.sum()

# Distancia ideal del trayecto
net_displacement = np.hypot(x[-1] - x[0], y[-1] - y[0])

# Relación entre velocidad lineal y angular:
v_lin = lineal_velocity()[1:]
w_abs = np.abs(angular_velocity())
corr = np.corrcoef(v_lin, w_abs)[0, 1]


def acceleration():
    return derivar(lineal_velocity(), t[1:])


# Puntos por los que se haya pasado +1 vez
_, inverse, counts = np.unique(data[['x', 'y']], return_inverse=True, return_counts=True)
visits = counts[inverse]
repeated = visits > 1



## Apartado C


def reconstruct_angle(theta_origin, omega, t):
    theta = theta_origin + np.cumsum(omega*delta(t[1:]))
    return theta

def reconstruct_v_vectors(theta, v,  t):
    vx = v*np.cos(theta) * delta(t)
    vy = v*np.sin(theta) * delta(t)
    return vx, vy

reconstruc = lambda coordinate, v: np.concatenate(([coordinate[0]], coordinate[0] + np.cumsum(v)))
