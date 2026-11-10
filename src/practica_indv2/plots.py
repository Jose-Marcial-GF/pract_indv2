import numpy as np
import matplotlib.pyplot as plt
from amopython import *


v = lineal_velocity()
w = angular_velocity()
alpha = derivar(w, t[2:])


## Apartado A
plt.figure(figsize=(12, 4))
plt.subplot(121)
plt.plot(t[1:], v)
plt.xlabel('t [s]')
plt.ylabel('v [m/s]')
plt.title('(a) Velocidad lineal')
plt.subplot(122)
plt.plot(t[2:], w, color='orange')
plt.xlabel('t [s]')
plt.ylabel('ω [rad/s]')
plt.title('(b) Velocidad angular')
plt.tight_layout()
plt.show()


## Apartado B
plt.figure(figsize=(12, 12))
plt.subplot(321)
plt.scatter(x[1:], y[1:], c=v, cmap='Blues', s=1)
plt.colorbar(label='v [m/s]')
plt.axis('equal')
plt.title('(a) Trayectoria coloreada por velocidad lineal')

plt.subplot(322)
plt.hist(dt * 1000, bins=np.arange(15, 240, 3))
plt.yscale('log')
plt.xlabel('Δt [ms]')
plt.title('(b) Periodo de muestreo Δt')

plt.subplot(323)
plt.scatter(w_abs, v_lin, s=1, alpha=0.4)
plt.xscale('symlog', linthresh=1)
plt.xlabel('|ω| [rad/s]')
plt.ylabel('v [m/s]')
plt.title(f'(c) Velocidad lineal frente a angular (r = {corr:.2f})')

plt.subplot(324)
plt.plot(x, y, color='lightgray', label='Recorrido')
plt.scatter(x[repeated], y[repeated], color='orange', label='Puntos repetidos')
plt.axis('equal')
plt.legend()
plt.title('(d) Puntos visitados más de una vez')

plt.subplot(325)
plt.plot(t[2:], acceleration())
plt.xlabel('t [s]')
plt.ylabel('a [m/s²]')
plt.title('(e) Aceleración lineal')

plt.subplot(326)
plt.plot(t[3:], alpha, color='orange')
plt.xlabel('t [s]')
plt.ylabel('α [rad/s²]')
plt.title('(f) Aceleración angular')
plt.tight_layout()
plt.show()


## Apartado C
theta_rec = lambda omega: np.concatenate(([theta[0]], reconstruct_angle(theta[0], omega, t)))

def reconstruct(v, w):
    vx, vy = reconstruct_v_vectors(theta_rec(w), v, t)
    return reconstruc(x, vx), reconstruc(y, vy)

v_noised = v + np.random.normal(0, 0.01 * np.mean(v), size=len(v))
w_noised = w + np.random.normal(0, 0.01 * np.mean(np.abs(w)), size=len(w))

plt.figure(figsize=(12, 4))
cases = [('(a) Sin ruido', v, w), ('(b) Ruido en v', v_noised, w), ('(c) Ruido en ω', v, w_noised)]
for i, (title, v_case, w_case) in enumerate(cases):
    plt.subplot(131 + i)
    plt.plot(x, y, linewidth=3, alpha=0.5, label='Original')
    plt.plot(*reconstruct(v_case, w_case), '--', label='Reconstruida')
    plt.axis('equal')
    plt.title(title)
    plt.legend()
plt.tight_layout()
plt.show()
