import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

OUT = "/home/user/Fincontrol/fotos"
os.makedirs(OUT, exist_ok=True)

# ── estilo boceto simple ─────────────────────────────────────────────────
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
})

def save(fig, name):
    path = f"{OUT}/{name}"
    fig.savefig(path, dpi=110, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  ✓ {path}")


# ─── 1. Canal Parabólico ────────────────────────────────────────────────
def canal_parabolico():
    fig, ax = plt.subplots(figsize=(6, 3.8), facecolor="#f9f9f9")
    ax.set_facecolor("#f9f9f9")
    x = np.linspace(-3.5, 3.5, 300)
    y = x**2 / 5
    ax.fill_between(x, y - 0.15, y, color="#a8c8e8", alpha=0.9)
    ax.plot(x, y, color="#2255aa", lw=2)
    # tubo receptor
    circ = plt.Circle((0, 2.45), 0.18, color="#c0392b", zorder=5)
    ax.add_patch(circ)
    ax.text(0.25, 2.45, "Tubo receptor", fontsize=8, va="center", color="#c0392b")
    # rayos
    for xi in [-2.8, -1.5, 0, 1.5, 2.8]:
        ax.annotate("", xy=(xi, xi**2/5), xytext=(xi, 4.5),
                    arrowprops=dict(arrowstyle="-|>", color="#f1c40f", lw=1.3))
        ax.plot([xi, 0], [xi**2/5, 2.45], "--", color="#f1c40f", lw=0.9, alpha=0.7)
    ax.set_xlim(-4, 5); ax.set_ylim(-0.2, 5)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("Colector de Canal Parabólico (CCP)", fontsize=10, pad=6, color="#222")
    save(fig, "2d_canal_parabolico.png")

# ─── 2. Fresnel Lineal ──────────────────────────────────────────────────
def fresnel_lineal():
    fig, ax = plt.subplots(figsize=(6, 3.8), facecolor="#f9f9f9")
    ax.set_facecolor("#f9f9f9")
    espejos_x = np.linspace(-3.5, 3.5, 9)
    rx, ry = 0, 3.2
    for xi in espejos_x:
        ang = np.degrees(np.arctan2(ry - 0, rx - xi)) / 2
        dx = 0.35 * np.cos(np.radians(ang))
        dy = 0.35 * np.sin(np.radians(ang))
        ax.plot([xi-dx, xi+dx], [-dy, dy], color="#2255aa", lw=4, solid_capstyle="round")
        ax.annotate("", xy=(xi, 0), xytext=(xi, 2.4),
                    arrowprops=dict(arrowstyle="-|>", color="#f1c40f", lw=1))
        ax.plot([xi, rx], [0, ry], "--", color="#f1c40f", lw=0.8, alpha=0.55)
    ax.fill_between([-0.6, 0.6], [ry-0.1], [ry+0.1], color="#c0392b")
    ax.text(0.7, ry, "Receptor", fontsize=8, va="center", color="#c0392b")
    ax.set_xlim(-4.5, 4.5); ax.set_ylim(-0.5, 4.2)
    ax.axis("off")
    ax.set_title("Concentrador de Fresnel Lineal (LFC)", fontsize=10, pad=6, color="#222")
    save(fig, "2d_fresnel_lineal.png")

# ─── 3. CPC Winston ─────────────────────────────────────────────────────
def cpc_winston():
    fig, ax = plt.subplots(figsize=(5, 5), facecolor="#f9f9f9")
    ax.set_facecolor("#f9f9f9")
    th = np.radians(22)
    a = 0.5
    t = np.linspace(0, 2.0, 300)
    f = 4 * a * (1 + np.sin(th))
    lx = -a - (t**2/f)*np.cos(th) + t*np.sin(th)
    ly =      (t**2/f)*np.sin(th) + t*np.cos(th)
    rx =  a + (t**2/f)*np.cos(th) - t*np.sin(th)
    ry =      (t**2/f)*np.sin(th) + t*np.cos(th)
    ax.plot(lx, ly, color="#2255aa", lw=2.2)
    ax.plot(rx, ry, color="#2255aa", lw=2.2)
    ax.fill_between([-a, a], [-0.04], [0.04], color="#c0392b")
    ax.text(a+0.08, 0, "Receptor", fontsize=8, va="center", color="#c0392b")
    # rayos aceptados
    for xi in [-0.6, -0.2, 0.2, 0.6]:
        ax.annotate("", xy=(xi, 0), xytext=(xi+0.35, max(ly)-0.05),
                    arrowprops=dict(arrowstyle="-|>", color="#f1c40f", lw=1.1, alpha=0.85))
    ax.text(0, max(ly)+0.15, "Apertura", fontsize=8, ha="center", color="#27ae60")
    ax.set_xlim(-2.2, 2.5); ax.set_ylim(-0.3, max(ly)+0.5)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("CPC — Concentrador Parabólico Compuesto (Winston)", fontsize=9.5, pad=6, color="#222")
    save(fig, "2d_cpc_winston.png")

# ─── 4. Disco Parabólico 3D ─────────────────────────────────────────────
def disco_parabolico():
    fig = plt.figure(figsize=(6, 4.5), facecolor="#f9f9f9")
    ax = fig.add_subplot(111, projection="3d", facecolor="#f9f9f9")
    r = np.linspace(0, 2, 30)
    th = np.linspace(0, 2*np.pi, 50)
    R, T = np.meshgrid(r, th)
    X = R*np.cos(T); Y = R*np.sin(T); Z = -(X**2+Y**2)/3
    ax.plot_surface(X, Y, Z, alpha=0.5, color="#a8c8e8",
                    edgecolor="#2255aa", linewidth=0.15, rstride=2, cstride=2)
    ax.scatter([0],[0],[1.33], color="#c0392b", s=90, zorder=10)
    ax.text(0.1, 0.1, 1.6, "Receptor", fontsize=8, color="#c0392b")
    for xi,yi in [(-1.4,0),(1.4,0),(0,-1.4),(0,1.4),(-1,1),(1,-1)]:
        zi = -(xi**2+yi**2)/3
        ax.quiver(xi, yi, 2.5, 0, 0, zi-2.5, color="#f1c40f",
                  arrow_length_ratio=0.2, lw=1.2, alpha=0.8)
        ax.plot([xi,0],[yi,0],[zi,1.33], "--", color="#f1c40f", lw=0.7, alpha=0.5)
    ax.set_axis_off()
    ax.view_init(elev=22, azim=-50)
    ax.set_title("Disco Parabólico", fontsize=10, pad=4, color="#222")
    save(fig, "3d_disco_parabolico.png")

# ─── 5. Torre Solar ─────────────────────────────────────────────────────
def torre_solar():
    fig, ax = plt.subplots(figsize=(6, 5), facecolor="#e8f4ea")
    ax.set_facecolor("#e8f4ea")
    # suelo
    ax.fill_between([-7, 7], [-0.3], [0], color="#8B7355", alpha=0.6)
    # torre
    ax.fill_between([-0.2, 0.2], [0], [5.5], color="#888888")
    ax.fill_between([-0.35, 0.35], [5.3], [5.7], color="#c0392b")
    ax.text(0.4, 5.5, "Receptor", fontsize=8, va="center", color="#c0392b")
    # heliostatos
    np.random.seed(7)
    n = 40
    angs = np.random.uniform(0, 2*np.pi, n)
    rados = np.random.uniform(1.5, 5.5, n)
    hxs = rados*np.cos(angs); hys = rados*np.sin(angs)*0.45
    for hx, hy in zip(hxs, hys):
        ax.fill_between([hx-0.25, hx+0.25], [hy-0.05], [hy+0.05],
                        color="#a8c8e8", alpha=0.85)
        ax.plot([hx-0.25, hx+0.25], [hy+0.05, hy+0.05], color="#2255aa", lw=0.8)
        ax.plot([hx, 0], [hy, 5.5], color="#f1c40f", lw=0.4, alpha=0.3)
    # sol
    sol = plt.Circle((5.5, 6.0), 0.5, color="#f1c40f", zorder=5)
    ax.add_patch(sol)
    ax.text(5.5, 6.7, "Sol", fontsize=8, ha="center", color="#e67e22", fontweight="bold")
    ax.set_xlim(-6.5, 7); ax.set_ylim(-0.5, 7.5)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("Torre Solar con Campo de Heliostatos", fontsize=10, pad=6, color="#222")
    save(fig, "3d_torre_solar.png")

# ─── 6. Lente de Fresnel Circular ───────────────────────────────────────
def fresnel_circular():
    fig, ax = plt.subplots(figsize=(6, 4.2), facecolor="#f9f9f9")
    ax.set_facecolor("#f9f9f9")
    ly = 3.2; f = 2.8; lh = 2.2
    n_z = 10
    edges = np.linspace(-lh, lh, n_z*2+1)
    for i in range(len(edges)-1):
        x0, x1 = edges[i], edges[i+1]
        xc = (x0+x1)/2
        h = 0.13*(1 - abs(xc)/lh)
        c = "#a8c8e8" if i%2==0 else "#cce4f5"
        ax.fill_between([x0, x1], [ly], [ly+h], color=c, edgecolor="#2255aa", lw=0.4)
    ax.fill_between([-lh, lh], [ly-0.08], [ly], color="#a8c8e8", alpha=0.7)
    ax.plot([-lh, lh], [ly-0.08, ly-0.08], color="#2255aa", lw=1.5)
    fp_y = ly - f
    ax.scatter([0], [fp_y], color="#c0392b", s=80, zorder=8)
    ax.text(0.15, fp_y, "Punto focal", fontsize=8, va="center", color="#c0392b")
    for xi in np.linspace(-1.8, 1.8, 7):
        ax.annotate("", xy=(xi, ly+0.12), xytext=(xi, ly+1.3),
                    arrowprops=dict(arrowstyle="-|>", color="#f1c40f", lw=1.1))
        ax.plot([xi, 0], [ly, fp_y], "--", color="#f1c40f", lw=0.8, alpha=0.6)
    ax.annotate("", xy=(lh+0.3, fp_y), xytext=(lh+0.3, ly),
                arrowprops=dict(arrowstyle="<->", color="#27ae60", lw=1.1))
    ax.text(lh+0.45, (fp_y+ly)/2, f"f", fontsize=9, va="center", color="#27ae60")
    ax.set_xlim(-3, 4); ax.set_ylim(fp_y-0.3, ly+1.8)
    ax.axis("off")
    ax.set_title("Lente de Fresnel Circular (CPV)", fontsize=10, pad=6, color="#222")
    save(fig, "3d_fresnel_circular.png")


print("Generando imágenes...")
canal_parabolico()
fresnel_lineal()
cpc_winston()
disco_parabolico()
torre_solar()
fresnel_circular()
print("Listo.")
