import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt



delta = lambda data : np.diff(data)
v = lambda points, time : delta(points) / delta(time)

data = np.loadtxt(
    Path(__file__).parent / "resources/path_SRA2526.txt",
    dtype=[("x", float), ("y", float), ("t", float)],
)
x = data['x']
y = data['y']
t = data['t']


## Apartado A
def lineal_velocity(data):
    return np.hypot(delta(x), delta(y))/delta(t)

theta = np.unwrap(np.arctan2(v(y, t), v(x, t)))
def angular_velocity(data):
    theta = np.unwrap(np.arctan2(v(y, t), v(x, t)))
    return np.diff(theta) / np.diff(data['t'][1:])

plt.subplot(131)
plt.plot(data['x'], data['y'])
plt.scatter(data['x'][0], data['y'][0], color='red')
plt.subplot(132)
print(np.max(angular_velocity(data)))
plt.plot(data['t'][2:], angular_velocity(data))
plt.subplot(133)
plt.plot( data['t'][1:], lineal_velocity(data))
plt.show()


## Apartado B
# Periodicidad de las medidas de tiempo
dt = delta(t)
print(f"dt medio: {dt.mean():.4f} s | mediana: {np.median(dt):.4f} s | "
      f"mín: {dt.min():.4f} s | máx: {dt.max():.4f} s | std: {dt.std():.4f} s")


# Distancia recorrida, duración y desplazamiento neto
step = np.hypot(delta(x), delta(y))
# cada cuanta distancia nos da una nueva posición
step.mean()
#cuanto fue lo máximo que avanzó sin dar información
step.max()

# Distancia recorrida
total_distance = step.sum()
# tiempo de recorrido
duration = t[-1] - t[0]

# Distancia ideal del trayecto
net_displacement = np.hypot(x[-1] - x[0], y[-1] - y[0])

print(f"Distancia total recorrida: {total_distance:.3f} m")
print(f"Duración: {duration:.3f} s")
print(f"Velocidad media global (distancia / duración): {total_distance / duration:.3f} m/s")
print(f"Desplazamiento neto inicio-fin: {net_displacement:.3f} m "
      f"({100 * net_displacement / total_distance:.2f} % de la distancia)")

# Relación entre velocidad lineal y angular:
# ¿frena el robot cuando gira? 
v_lin = lineal_velocity(data)[1:]
w_abs = np.abs(angular_velocity(data))
corr = np.corrcoef(v_lin, w_abs)[0, 1]
print(f"Correlación v vs |ω|: {corr:.3f}")
# Aceleración lateral (centrípeta) a = v·|ω|: limita deslizamiento/vuelco en curvas
print(f"Aceleración lateral máxima: {np.max(v_lin * w_abs):.3f} m/s²")

plt.scatter(w_abs, v_lin, s=5)
plt.xlabel('|ω| [rad/s]')
plt.ylabel('v [m/s]')
plt.title(f'Velocidad lineal vs angular (r = {corr:.2f})')
plt.show()
# Velocidad Máxima con los T para poder graficarlo
print(np.argmax(lineal_velocity(data)))

# Velocidad media
print(np.mean(lineal_velocity(data)))

# Velocidad mínima
print(np.min(lineal_velocity(data)))


# Velocidad Máxima con los T para poder graficarlo
print(np.argmax(angular_velocity(data)))

# Velocidad media
print(np.mean(angular_velocity(data)))

# Velocidad mínima
print(np.min(angular_velocity(data)))


def acceleration(data):
    return v(lineal_velocity(data), t[1:])
    

# Aceleración Máxima con los T para poder graficarlo
print(acceleration(data))

# Aceleración máxima
np.mean(acceleration(data))

# Aceleración media
np.mean(acceleration(data))

# Aceleración Minima
np.min(acceleration(data))

# Puntos por los que se haya pasado +1 vez
_, inverse, counts = np.unique(data[['x', 'y']], return_inverse=True, return_counts=True)
visits = counts[inverse]
repeated = visits > 1

plt.plot(x, y, color='lightgray', label='Recorrido')
plt.scatter(x[repeated], y[repeated], cmap='autumn_r', s=30, label='Puntos repetidos')
# media de visitas por puntos para saber si repites muchas veces el mismo recorridoplt.show()
plt.show()



## Apartado C


def reconstruct_angle(theta_origin, omega, t):
    theta = theta_origin + np.cumsum(omega*delta(t[1:]))
    return theta

def reconstruct_v_vectors(theta, v,  t):
    vx = v*np.cos(theta) * delta(t)
    vy = v*np.sin(theta) * delta(t)
    return vx, vy



    
theta_reconstruct = reconstruct_angle(theta[0], angular_velocity(data), t)
vx, vy = reconstruct_v_vectors(np.concatenate(([theta[0]], theta_reconstruct)),  lineal_velocity(data), t)

reconstructed_x = np.concatenate(([x[0]], x[0] + np.cumsum(vx)))
reconstructed_y = np.concatenate(([y[0]], y[0] + np.cumsum(vy)))


sigma_v = 0.0
sigma_omega = 0.02

# 2. Sumas el ruido gaussiano a tus vectores de velocidad originales
v_ruido = lineal_velocity + np.random.normal(0, sigma_v, size=len(v))
omega_ruido = velocidad_a+ np.random.normal(0, sigma_omega, size=len(velocidad_angular))

plt.figure(figsize=(8, 6))
plt.plot(data['x'], data['y'], label='Original', linewidth=3, alpha=0.5)
plt.plot(reconstructed_x, reconstructed_y, '--r', label='Reconstruida desde v y ω')
plt.legend()
plt.legend()
plt.title("Comparación: Trayectoria Original vs Reconstruida")
plt.show()
