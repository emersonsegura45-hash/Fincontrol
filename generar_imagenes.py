import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, Arc, Wedge
from matplotlib.path import Path
import matplotlib.patheffects as pe
import os

OUT = "/home/user/Fincontrol/imgs"
os.makedirs(OUT, exist_ok=True)

BG   = "#f7f9fc"
BLUE = "#1a4fa0"
LB   = "#5b9bd5"
RED  = "#c0392b"
ORG  = "#e67e22"
GRY  = "#7f8c8d"
YEL  = "#f1c40f"
GRN  = "#27ae60"


# ─────────────────────────────────────────────
# 1. Canal Parabólico (CCP)
# ─────────────────────────────────────────────
def fig_canal_parabolico():
    fig, ax = plt.subplots(figsize=(7, 4), facecolor=BG)
    ax.set_facecolor(BG)

    # Parabola y = x²/4  (foco en y=1)
    x = np.linspace(-4, 4, 400)
    y = x**2 / 4
    ax.fill_between(x, y - 0.18, y, color=LB, alpha=0.85, zorder=2)
    ax.plot(x, y, color=BLUE, lw=2, zorder=3)

    # Tubo receptor en foco (y=1)
    tube = plt.Circle((0, 1), 0.18, color=RED, zorder=5)
    ax.add_patch(tube)
    ax.text(0.25, 1, "Tubo\nreceptor", fontsize=7.5, color=RED, va="center", zorder=6)

    # Rayos solares entrantes (paralelos, verticales)
    for xi in np.linspace(-3.5, 3.5, 8):
        yi_start = 5
        yi_hit   = xi**2 / 4
        ax.annotate("", xy=(xi, yi_hit), xytext=(xi, yi_start),
                    arrowprops=dict(arrowstyle="-|>", color=YEL, lw=1.3))
        # Rayo reflejado hacia foco
        ax.plot([xi, 0], [yi_hit, 1], color=YEL, lw=0.9, ls="--", alpha=0.7)

    ax.set_xlim(-4.5, 4.5)
    ax.set_ylim(-0.3, 5.5)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Colector de Canal Parabólico (CCP)", fontsize=11,
                 fontweight="bold", color=BLUE, pad=8)

    # eje focal
    ax.axhline(1, color=GRY, lw=0.8, ls=":", alpha=0.6)
    ax.text(-4.3, 1.05, "Eje focal", fontsize=7, color=GRY)

    fig.tight_layout()
    path = f"{OUT}/2d_1_canal_parabolico.png"
    fig.savefig(path, dpi=130, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  ✓ {path}")


# ─────────────────────────────────────────────
# 2. Fresnel Lineal
# ─────────────────────────────────────────────
def fig_fresnel_lineal():
    fig, ax = plt.subplots(figsize=(7, 4), facecolor=BG)
    ax.set_facecolor(BG)

    receptor_x, receptor_y = 0, 3.5
    n_mirrors = 9
    xs = np.linspace(-4, 4, n_mirrors)

    for xi in xs:
        # Ángulo de inclinación para reflejar hacia receptor
        angle_deg = np.degrees(np.arctan2(receptor_x - xi, receptor_y - 0)) / 2
        dx = 0.38 * np.cos(np.radians(angle_deg))
        dy = 0.38 * np.sin(np.radians(angle_deg))
        ax.plot([xi - dx, xi + dx], [-dy, dy], color=LB, lw=4, solid_capstyle="round", zorder=3)

        # Rayo incidente (vertical)
        ax.annotate("", xy=(xi, 0), xytext=(xi, 2.6),
                    arrowprops=dict(arrowstyle="-|>", color=YEL, lw=1.1))
        # Rayo reflejado
        ax.plot([xi, receptor_x], [0, receptor_y], color=YEL, lw=0.9, ls="--", alpha=0.65)

    # Receptor
    ax.fill_between([-0.55, 0.55], [receptor_y - 0.12], [receptor_y + 0.12],
                    color=RED, zorder=5)
    ax.text(0.6, receptor_y, "Receptor\nfijo", fontsize=7.5, color=RED, va="center")

    ax.set_xlim(-4.8, 4.8)
    ax.set_ylim(-0.5, 4.5)
    ax.axis("off")
    ax.set_title("Concentrador de Fresnel Lineal (LFC)", fontsize=11,
                 fontweight="bold", color=BLUE, pad=8)
    fig.tight_layout()
    path = f"{OUT}/2d_2_fresnel_lineal.png"
    fig.savefig(path, dpi=130, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  ✓ {path}")


# ─────────────────────────────────────────────
# 3. CPC de Winston (2D)
# ─────────────────────────────────────────────
def fig_cpc_winston():
    fig, ax = plt.subplots(figsize=(6, 5), facecolor=BG)
    ax.set_facecolor(BG)

    theta_a = np.radians(20)   # ángulo de aceptancia
    a = 0.5                    # semiancho receptor

    # Parábola izquierda: foco en (+a, 0), eje inclinado -theta_a
    # Parábola derecha:   foco en (-a, 0), eje inclinado +theta_a
    def parabola_cpc(side, n=300):
        # En coordenadas del CPC ideal simplificado
        t = np.linspace(0, np.pi * 1.35, n)
        r_focus = a
        # Parábola en coordenadas polares desde foco
        p = 2 * r_focus * (1 + np.sin(theta_a))  # semilatus rectum
        if side == "left":
            phi = t - (np.pi/2 + theta_a)
            r = p / (1 - np.cos(t))
            r = np.clip(r, 0, 8)
            px = -r_focus + r * np.cos(phi)
            py =           r * np.sin(phi)
        else:
            phi = t - (np.pi/2 + theta_a)
            r = p / (1 - np.cos(t))
            r = np.clip(r, 0, 8)
            px =  r_focus - r * np.cos(phi)
            py =            r * np.sin(phi)
        return px, py

    # Simplified clean CPC shape using parametric definition
    # Left mirror: parabola with focus at (a, 0), axis tilted by theta_a
    def left_mirror():
        f = a
        y_arr = np.linspace(0, 6, 400)
        # Classic CPC: left wall x(y) from parabola
        x_arr = -(f + y_arr * np.sin(theta_a) -
                  np.sqrt((y_arr + f * np.sin(theta_a))**2 + 0) )
        # Use direct CPC formula
        # x_L = (f(1 + sin θ) - y) / tan(θ + arcsin(sinθ·y/(f+y sinθ)))  ← complex
        # Simpler: straight parabola mirrored
        t = np.linspace(0, 2.2, 400)
        px = -a - t**2 / (4 * a * (1 + np.sin(theta_a))) * np.cos(theta_a) + t * np.sin(theta_a)
        py =  0 + t**2 / (4 * a * (1 + np.sin(theta_a))) * np.sin(theta_a) + t * np.cos(theta_a)
        return px, py

    def right_mirror():
        t = np.linspace(0, 2.2, 400)
        px =  a + t**2 / (4 * a * (1 + np.sin(theta_a))) * np.cos(theta_a) - t * np.sin(theta_a)
        py =  0 + t**2 / (4 * a * (1 + np.sin(theta_a))) * np.sin(theta_a) + t * np.cos(theta_a)
        return px, py

    lx, ly = left_mirror()
    rx, ry = right_mirror()

    ax.plot(lx, ly, color=BLUE, lw=2.5, zorder=3)
    ax.plot(rx, ry, color=BLUE, lw=2.5, zorder=3)

    # Fill mirror surfaces
    ax.fill_betweenx(ly, lx, lx - 0.08, color=LB, alpha=0.7)
    ax.fill_betweenx(ry, rx, rx + 0.08, color=LB, alpha=0.7)

    # Receptor (abajo)
    ax.fill_between([-a, a], [-0.05], [0.05], color=RED, zorder=5, lw=2)
    ax.text(a + 0.1, 0, "Receptor", fontsize=8, color=RED, va="center")

    # Ángulo de aceptancia
    y_top = max(ly[-1], ry[-1])
    ax.annotate("", xy=(lx[-1], ly[-1]), xytext=(rx[-1], ry[-1]),
                arrowprops=dict(arrowstyle="<->", color=GRN, lw=1.2))
    ax.text(0, y_top + 0.15, "Apertura", fontsize=8, color=GRN, ha="center")

    # Rayos dentro del ángulo de aceptancia
    for xi in [-0.55, 0, 0.55]:
        ax.annotate("", xy=(xi, 0), xytext=(xi + 0.4, y_top - 0.1),
                    arrowprops=dict(arrowstyle="-|>", color=YEL, lw=1.1, alpha=0.8))

    # Ángulo de aceptancia arc
    arc = Arc((0, y_top - 0.05), 0.7, 0.7, angle=90,
              theta1=-np.degrees(theta_a)*1.5, theta2=np.degrees(theta_a)*1.5,
              color=GRN, lw=1.2, ls="--")
    ax.add_patch(arc)
    ax.text(0.42, y_top + 0.35, f"θa = {int(np.degrees(theta_a))}°", fontsize=7.5, color=GRN)

    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-0.4, 3.2)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Concentrador Parabólico Compuesto — CPC (Winston 2D)", fontsize=10,
                 fontweight="bold", color=BLUE, pad=8)
    fig.tight_layout()
    path = f"{OUT}/2d_3_cpc_winston.png"
    fig.savefig(path, dpi=130, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  ✓ {path}")


# ─────────────────────────────────────────────
# 4. Disco Parabólico (3D)
# ─────────────────────────────────────────────
def fig_disco_parabolico():
    fig = plt.figure(figsize=(7, 5), facecolor=BG)
    ax = fig.add_subplot(111, projection="3d", facecolor=BG)

    r = np.linspace(0, 2, 40)
    theta = np.linspace(0, 2 * np.pi, 60)
    R, T = np.meshgrid(r, theta)
    X = R * np.cos(T)
    Y = R * np.sin(T)
    Z = -(X**2 + Y**2) / 3   # paraboloid abierto hacia abajo

    ax.plot_surface(X, Y, Z, alpha=0.55, color=LB, edgecolor=BLUE, linewidth=0.2,
                    rstride=2, cstride=2)

    # Punto focal
    ax.scatter([0], [0], [1.33], color=RED, s=120, zorder=10)
    ax.text(0.1, 0.1, 1.55, "Receptor\n(punto focal)", fontsize=8, color=RED)

    # Rayos entrantes
    for xi, yi in [(-1.5, 0), (1.5, 0), (0, -1.5), (0, 1.5), (-1, -1), (1, 1)]:
        zi_hit = -(xi**2 + yi**2) / 3
        ax.quiver(xi, yi, 2.5, 0, 0, zi_hit - 2.5, color=YEL, arrow_length_ratio=0.18,
                  linewidth=1.2, alpha=0.85)
        ax.plot([xi, 0], [yi, 0], [zi_hit, 1.33], color=YEL, lw=0.8, ls="--", alpha=0.6)

    ax.set_axis_off()
    ax.set_title("Disco Parabólico (Paraboloide de Revolución)", fontsize=11,
                 fontweight="bold", color=BLUE, pad=5)
    ax.view_init(elev=25, azim=-55)
    fig.tight_layout()
    path = f"{OUT}/3d_1_disco_parabolico.png"
    fig.savefig(path, dpi=130, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  ✓ {path}")


# ─────────────────────────────────────────────
# 5. Torre Solar con Heliostatos
# ─────────────────────────────────────────────
def fig_torre_solar():
    fig, ax = plt.subplots(figsize=(7, 5), facecolor=BG)
    ax.set_facecolor(BG)

    np.random.seed(42)
    n = 55
    angles = np.random.uniform(0, 2 * np.pi, n)
    radii  = np.random.uniform(1.8, 5.0, n)
    hx = radii * np.cos(angles)
    hy = radii * np.sin(angles)

    # Torre
    tower = plt.Rectangle((-0.18, -0.18), 0.36, 5.2, color=GRY, zorder=4)
    ax.add_patch(tower)
    receptor = plt.Circle((0, 5.2), 0.28, color=RED, zorder=5)
    ax.add_patch(receptor)
    ax.text(0.35, 5.2, "Receptor\n(torre)", fontsize=7.5, color=RED, va="center")

    # Heliostatos y rayos
    for xi, yi in zip(hx, hy):
        # Espejo pequeño
        ang = np.degrees(np.arctan2(5.2 - yi, 0 - xi)) + 45
        rect = mpatches.FancyBboxPatch(
            (xi - 0.22, yi - 0.1), 0.44, 0.2,
            boxstyle="round,pad=0.02",
            linewidth=0.5, edgecolor=BLUE,
            facecolor=LB, alpha=0.75,
            transform=ax.transData, zorder=3
        )
        ax.add_patch(rect)
        # Rayo reflejado
        ax.plot([xi, 0], [yi, 5.2], color=YEL, lw=0.5, alpha=0.35)

    # Sol (fuera del campo, arriba-derecha)
    sun = plt.Circle((6.5, 6.5), 0.55, color=YEL, zorder=6)
    ax.add_patch(sun)
    ax.text(6.5, 7.3, "Sol", fontsize=8, ha="center", color=ORG, fontweight="bold")

    # Rayos desde sol hacia heliostatos (muestra)
    for xi, yi in zip(hx[:6], hy[:6]):
        ax.annotate("", xy=(xi, yi), xytext=(6.5, 6.5),
                    arrowprops=dict(arrowstyle="-|>", color=YEL, lw=0.8, alpha=0.5))

    ax.set_xlim(-6, 8)
    ax.set_ylim(-6, 8)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Torre Solar con Campo de Heliostatos", fontsize=11,
                 fontweight="bold", color=BLUE, pad=8)
    fig.tight_layout()
    path = f"{OUT}/3d_2_torre_solar.png"
    fig.savefig(path, dpi=130, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  ✓ {path}")


# ─────────────────────────────────────────────
# 6. Lente de Fresnel Circular (3D)
# ─────────────────────────────────────────────
def fig_fresnel_circular():
    fig, ax = plt.subplots(figsize=(7, 5), facecolor=BG)
    ax.set_facecolor(BG)

    # Vista lateral: sección transversal de la lente de Fresnel
    focal = 3.0
    lens_y = 3.5
    lens_half = 2.5
    n_zones = 9

    xs_full = np.linspace(-lens_half, lens_half, 500)

    # Dibujar zonas de Fresnel (escalones)
    zone_edges = np.linspace(-lens_half, lens_half, n_zones * 2 + 1)
    colors_zones = [LB if i % 2 == 0 else "#a8d8f0" for i in range(len(zone_edges) - 1)]

    for i in range(len(zone_edges) - 1):
        x0, x1 = zone_edges[i], zone_edges[i + 1]
        xc = (x0 + x1) / 2
        # Altura del escalón según la zona
        base_h = lens_y
        step_h = 0.12 * (1 - abs(xc) / lens_half)  # taper
        # Perfil inclinado del escalón (simula la cara refractante)
        ax.fill_between([x0, x1], [base_h, base_h],
                        [base_h + step_h, base_h + step_h + 0.01 * (x1 - x0)],
                        color=colors_zones[i], alpha=0.85, edgecolor=BLUE, lw=0.4)

    # Base de la lente (plana abajo)
    ax.fill_between([-lens_half, lens_half], [lens_y - 0.1], [lens_y],
                    color=LB, alpha=0.5)
    ax.plot([-lens_half, lens_half], [lens_y - 0.1, lens_y - 0.1], color=BLUE, lw=1.5)

    # Punto focal
    focal_y = lens_y - focal
    ax.scatter([0], [focal_y], color=RED, s=120, zorder=10)
    ax.text(0.15, focal_y, "Punto focal", fontsize=8, color=RED, va="center")

    # Rayos solares entrantes (paralelos verticales)
    for xi in np.linspace(-2.2, 2.2, 8):
        ax.annotate("", xy=(xi, lens_y + 0.15), xytext=(xi, lens_y + 1.5),
                    arrowprops=dict(arrowstyle="-|>", color=YEL, lw=1.2))
        # Rayo refractado hacia focal
        ax.plot([xi, 0], [lens_y, focal_y], color=YEL, lw=0.9, ls="--", alpha=0.65)

    # Distancia focal
    ax.annotate("", xy=(lens_half + 0.3, focal_y), xytext=(lens_half + 0.3, lens_y),
                arrowprops=dict(arrowstyle="<->", color=GRN, lw=1.2))
    ax.text(lens_half + 0.45, (focal_y + lens_y) / 2, f"f = {focal} u",
            fontsize=7.5, color=GRN, va="center")

    ax.set_xlim(-3.5, 4.0)
    ax.set_ylim(focal_y - 0.5, lens_y + 2.0)
    ax.axis("off")
    ax.set_title("Lente de Fresnel Circular (sección transversal)", fontsize=11,
                 fontweight="bold", color=BLUE, pad=8)
    fig.tight_layout()
    path = f"{OUT}/3d_3_fresnel_circular.png"
    fig.savefig(path, dpi=130, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  ✓ {path}")


print("Generando diagramas...")
fig_canal_parabolico()
fig_fresnel_lineal()
fig_cpc_winston()
fig_disco_parabolico()
fig_torre_solar()
fig_fresnel_circular()
print("Listo.")
