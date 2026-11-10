"""Genera las figuras y los datos numéricos de la memoria (memoria.tex).

Reutiliza los resultados de src/practica_indv2/amopython.py (misma semilla, mismo
Monte Carlo) y escribe:
  - figuras/velocidades.pdf, figuras/analisis.pdf, figuras/errores.pdf
  - datos.tex  (macros \\newcommand con los valores que cita la memoria)

Uso, desde la raíz del repositorio:
    MPLBACKEND=Agg .venv/bin/python memoria/generar_figuras.py
"""
import contextlib
import io
import sys
import warnings
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "src"))

# Importar el módulo ejecuta todo el análisis; se silencian sus prints/plt.show()
warnings.filterwarnings("ignore")
with contextlib.redirect_stdout(io.StringIO()):
    from practica_indv2 import amopython as a
plt.close("all")

FIG_DIR = ROOT / "figuras"
FIG_DIR.mkdir(exist_ok=True)

# Ancho de texto en A4 con márgenes de 2 cm = 17 cm -> la figura se incluye a escala 1:1
TEXT_W = 17 / 2.54
BLUE, ORANGE, GRAY = "#2a78d6", "#eb6834", "#9a9893"
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["STIXGeneral"],  # Times-like con tildes; casa con newtx en LaTeX
    "mathtext.fontset": "stix",
    "font.size": 8,
    "axes.titlesize": 8,
    "axes.labelsize": 8,
    "legend.fontsize": 7,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.color": "#e4e3df",
    "grid.linewidth": 0.5,
    "axes.edgecolor": "#52514e",
    "legend.frameon": False,
    "legend.framealpha": 0.9,
    "legend.edgecolor": "none",
    "savefig.dpi": 300,
})

x, y, t, dt = a.x, a.y, a.t, a.dt
v, w = a.v_meas, a.w_meas
t_v, t_w = t[1:], t[2:]


def moving_average(s, n=35):
    """Media móvil centrada de n muestras (~1 s con el periodo medio de 29 ms)."""
    return np.convolve(s, np.ones(n) / n, mode="same")


# ---------------------------------------------------------------- Figura 1
W_CLIP = 12
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(TEXT_W, 3.0), sharex=True)
ax1.plot(t_v, v, color=BLUE, lw=0.4, alpha=0.45, label="calculada", rasterized=True)
ax1.plot(t_v, moving_average(v), color=BLUE, lw=1.0, label="media móvil 1 s")
ax1.set_ylabel(r"$v$ [m/s]")
ax1.set_ylim(0, None)
ax1.legend(loc="upper right", ncol=2, frameon=True)

ax2.plot(t_w, w, color=ORANGE, lw=0.3, alpha=0.35, label="calculada", rasterized=True)
ax2.plot(t_w, moving_average(w), color=ORANGE, lw=1.0, label="media móvil 1 s")
ax2.set_ylim(-W_CLIP, W_CLIP)
ax2.set_ylabel(r"$\omega$ [rad/s]")
ax2.set_xlabel(r"$t$ [s]")
ax2.legend(loc="upper right", ncol=2, frameon=True)
ax2.text(0.005, 0.04, rf"eje recortado a $\pm${W_CLIP} rad/s; picos aislados hasta "
         rf"$\pm${np.abs(w).max():.1f} rad/s", transform=ax2.transAxes,
         fontsize=6.5, color="#52514e",
         bbox=dict(facecolor="white", edgecolor="none", alpha=0.9, pad=1))
ax2.set_xlim(t[0], t[-1])
fig.align_ylabels()
fig.tight_layout(h_pad=0.4)
fig.savefig(FIG_DIR / "velocidades.pdf")
plt.close(fig)

# ---------------------------------------------------------------- Figura 2
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(TEXT_W, 2.5),
                               gridspec_kw={"width_ratios": [1.15, 1]})
v_max_c = np.percentile(v, 99)
# Se recorta el tramo más claro de "Blues" para que los tramos lentos sigan viéndose
blues = matplotlib.colors.ListedColormap(plt.get_cmap("Blues")(np.linspace(0.3, 1, 256)))
sc = ax1.scatter(x[1:], y[1:], c=v, cmap=blues, vmin=0, vmax=v_max_c, s=0.6,
                 lw=0, rasterized=True)
ax1.plot(x[0], y[0], "o", ms=5, mfc=ORANGE, mec="white", mew=0.8, label="inicio")
ax1.plot(x[-1], y[-1], "s", ms=5, mfc="#0b0b0b", mec="white", mew=0.8, label="fin")
ax1.set_aspect("equal")
ax1.set_xlabel(r"$x$ [m]")
ax1.set_ylabel(r"$y$ [m]")
ax1.set_title("(a) Trayectoria coloreada por velocidad lineal")
ax1.legend(loc="lower left", handletextpad=0.2)
cb = fig.colorbar(sc, ax=ax1, fraction=0.05, pad=0.02, extend="max")
cb.set_label(r"$v$ [m/s]")
cb.outline.set_visible(False)

ax2.hist(dt * 1000, bins=np.arange(15, 240, 3), color=BLUE, edgecolor="white", lw=0.3)
ax2.set_yscale("log")
ax2.axvline(np.median(dt) * 1000, color="#0b0b0b", lw=0.8, ls="--")
ax2.text(np.median(dt) * 1000 + 4, 0.92, f"mediana {np.median(dt) * 1000:.0f} ms",
         transform=ax2.get_xaxis_transform(), fontsize=7)
ax2.set_xlabel(r"$\Delta t$ [ms]")
ax2.set_ylabel("nº de intervalos")
ax2.set_title(r"(b) Periodo de muestreo $\Delta t$")
fig.tight_layout(w_pad=1.0)
fig.savefig(FIG_DIR / "analisis.pdf")
plt.close(fig)

# ---------------------------------------------------------------- Figura 3
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(TEXT_W, 2.5),
                               gridspec_kw={"width_ratios": [1.25, 1]})
ax1.plot(x, y, color=GRAY, lw=2.2, alpha=0.6, label="real")
ax1.plot(*a.traj_c2[0], color=BLUE, lw=0.6, label="c2 (ruido en $v$)")
ax1.plot(*a.traj_c3[0], color=ORANGE, lw=0.6, label=r"c3 (ruido en $\omega$)")
ax1.plot(a.x0, a.y0, "o", ms=5, mfc="#0b0b0b", mec="white", mew=0.8)
ax1.set_aspect("equal")
ax1.set_xlabel(r"$x$ [m]")
ax1.set_ylabel(r"$y$ [m]")
ax1.set_title("(a) Reconstrucción (una realización)")
ax1.legend(loc="upper left", bbox_to_anchor=(1.0, 1.0), handlelength=1.2,
           borderaxespad=0.2)

for name, errors, color in ((r"c2 (ruido en $v$)", a.errors_c2, BLUE),
                            (r"c3 (ruido en $\omega$)", a.errors_c3, ORANGE)):
    e = errors[:, 1:]
    ax2.plot(t[1:], e.mean(axis=0), color=color, lw=1.0, label=name)
    ax2.fill_between(t[1:], np.percentile(e, 5, axis=0), np.percentile(e, 95, axis=0),
                     color=color, alpha=0.18, lw=0, rasterized=True)
ax2.set_yscale("log")
ax2.set_ylim(1e-4, 10)
ax2.set_xlim(t[0], t[-1])
ax2.set_xlabel(r"$t$ [s]")
ax2.set_ylabel("error de posición [m]")
ax2.set_title(f"(b) Error medio y banda 5-95 % ({a.N_RUNS} realizaciones)")
ax2.legend(loc="lower right")
fig.tight_layout(w_pad=1.0)
fig.savefig(FIG_DIR / "errores.pdf")
plt.close(fig)


# ---------------------------------------------------------------- datos.tex
def f(value, nd=3):
    return f"{value:.{nd}f}"


def sci(value):
    """Notación científica en LaTeX: 1.2e-13 -> $1.2\times10^{-13}$."""
    mant, exp = f"{value:.1e}".split("e")
    return f"${mant}\\times10^{{{int(exp)}}}$"


def mc(errors, key):
    vals = np.array([a.error_metrics(e)[key] for e in errors])
    return vals.mean(), vals.std()


heading = np.unwrap(np.arctan2(np.diff(y), np.diff(x)))
acc = a.acceleration(a.data)
c1 = a.error_metrics(a.err_c1)

macros = {
    "Nmuestras": f"{len(x):,}".replace(",", "\\,"),
    "tIni": f(t[0], 1), "tFin": f(t[-1], 1), "duracion": f(a.duration, 1),
    "xMin": f(x.min(), 2), "xMax": f(x.max(), 2), "yMin": f(y.min(), 2), "yMax": f(y.max(), 2),
    "dtMedio": f(dt.mean() * 1000, 1), "dtMediana": f(np.median(dt) * 1000, 0),
    "dtMin": f(dt.min() * 1000, 0), "dtMax": f(dt.max() * 1000, 0),
    "dtStd": f(dt.std() * 1000, 1), "fMuestreo": f(1 / dt.mean(), 1),
    "nHuecos": str(int((dt > 0.1).sum())),
    "pasoMedio": f(a.step.mean() * 1000, 1), "pasoMax": f(a.step.max() * 1000, 1),
    "distancia": f(a.total_distance, 1), "vGlobal": f(a.total_distance / a.duration, 3),
    "desplNeto": f(a.net_displacement, 2),
    "desplPct": f(100 * a.net_displacement / a.total_distance, 2),
    "vMedia": f(v.mean(), 3), "vMax": f(v.max(), 2), "vMin": f(v.min(), 4),
    "vPnoventaycinco": f(np.percentile(v, 95), 2), "tvMax": f(t_v[np.argmax(v)], 1),
    "vLenta": f(100 * (v < 0.05).mean(), 1),
    "wMedia": f(w.mean(), 3), "wAbsMedia": f(np.abs(w).mean(), 2),
    "wAbsMediana": f(np.median(np.abs(w)), 2), "wMax": f(np.abs(w).max(), 2),
    "wSuaveAbsMedia": f(np.abs(moving_average(w)).mean(), 2),
    "giroNeto": f(heading[-1] - heading[0], 1),
    "vueltas": f((heading[-1] - heading[0]) / (2 * np.pi), 1),
    "corrVW": f(a.corr, 3), "aLatMax": f(np.max(a.v_lin * a.w_abs), 2),
    "aAbsMedia": f(np.abs(acc).mean(), 2), "aPuno": f(np.percentile(acc, 1), 2),
    "aPnoventaynueve": f(np.percentile(acc, 99), 2),
    "nRepetidos": str(int(a.repeated.sum())),
    "xCero": f(a.x0, 3), "yCero": f(a.y0, 3), "thetaCero": f(a.theta0, 3),
    "thetaCeroGrados": f(np.degrees(a.theta0), 1),
    "sigmaV": f(a.sigma_v, 5), "sigmaW": f(a.sigma_w, 4), "Nruns": str(a.N_RUNS),
    "cUnoFinal": sci(c1['final']), "cUnoMax": sci(c1['max']), "cUnoRmse": sci(c1['rmse']),
}
for tag, errors in (("cDos", a.errors_c2), ("cTres", a.errors_c3)):
    for key, name in (("final", "Final"), ("max", "Max"), ("rmse", "Rmse")):
        m, s = mc(errors, key)
        macros[f"{tag}{name}"] = f"{m:.4f}"
        macros[f"{tag}{name}Std"] = f"{s:.4f}"
    macros[f"{tag}Pct"] = f(100 * mc(errors, "final")[0] / a.total_distance, 4 if tag == "cDos" else 3)
macros["ratioErr"] = f"{mc(a.errors_c3, 'final')[0] / mc(a.errors_c2, 'final')[0]:.0f}"

# Tabla del apartado b): media, mediana, mínimo y máximo de cada magnitud
stats_rows = [
    (r"Periodo de muestreo $\Delta t$ [ms]", dt * 1000, 1),
    (r"Distancia entre muestras [mm]", a.step * 1000, 1),
    (r"Velocidad lineal $v$ [m/s]", v, 3),
    (r"Velocidad angular $\omega$ [rad/s]", w, 2),
    (r"$\omega$ filtrada (media móvil 1 s) [rad/s]", moving_average(w), 2),
    (r"Aceleración tangencial [m/s$^2$]", acc, 2),
    (r"Aceleración lateral $v|\omega|$ [m/s$^2$]", a.v_lin * a.w_abs, 2),
]
with open(ROOT / "tabla_estadisticos.tex", "w") as fh:
    fh.write("% Generado automáticamente por generar_figuras.py; no editar a mano.\n")
    for name, s, nd in stats_rows:
        vals = " & ".join(f"${val:.{nd}f}$" for val in
                          (s.mean(), np.median(s), s.min(), s.max()))
        fh.write(f"{name} & {vals} \\\\\n")

with open(ROOT / "datos.tex", "w") as fh:
    fh.write("% Generado automáticamente por generar_figuras.py; no editar a mano.\n")
    for k, val in macros.items():
        fh.write(f"\\newcommand{{\\{k}}}{{{val}}}\n")

print(f"Figuras en {FIG_DIR} y datos en {ROOT / 'datos.tex'}")
