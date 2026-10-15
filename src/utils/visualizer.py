"""
Módulo de Visualización y Generación de Reportes Gráficos.
Desacopla la lógica de renderizado gráfico de los motores algorítmicos.
"""

import os
from typing import Any, Dict, List, Optional
import matplotlib.pyplot as plt
import numpy as np

# Configuración estética global
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.titlesize": 14,
    "figure.dpi": 300,
    "lines.linewidth": 1.8,
    "lines.markersize": 6,
    "grid.alpha": 0.35,
    "grid.linestyle": "--"
})


class ParcialVisualizer:
    """
    Servicio de visualización para los resultados del Parcial 2.
    """

    def __init__(self, output_dir: Optional[str] = None):
        if output_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            self.output_dir = os.path.join(base_dir, "images")
        else:
            self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def plot_punto1_genetic(self, hist: Dict[str, List], multi_seed_hist: Dict[int, List[float]]) -> str:
        gens = hist["generation"]
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

        ax1.plot(gens, hist["best_fitness"], "o-", color="#1f77b4", label="Mejor Aptitud (Elitismo)")
        ax1.plot(gens, hist["average_fitness"], "s--", color="#ff7f0e", label="Aptitud Promedio")
        ax1.axhline(961, color="crimson", linestyle=":", linewidth=2, label="Óptimo Global Teórico (x=31, f=961)")
        ax1.set_title("Evolución de Aptitud (Semilla 42)", fontweight="bold")
        ax1.set_xlabel("Generación")
        ax1.set_ylabel("Aptitud $f(x) = x^2$")
        ax1.set_xticks(range(0, 21, 2))
        ax1.set_ylim(0, 1020)
        ax1.legend(loc="lower right")
        ax1.grid(True)

        colores = ["#1f77b4", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]
        for i, (seed, fits) in enumerate(multi_seed_hist.items()):
            label_str = f"Semilla {seed}" + (" (Oficial: Óptimo)" if seed == 42 else "")
            ax2.plot(gens, fits, marker=".", linewidth=1.6, color=colores[i % len(colores)], label=label_str)
        ax2.axhline(961, color="crimson", linestyle=":", linewidth=2, label="Óptimo Global (961)")
        ax2.set_title("Sensibilidad Estocástica (5 Semillas Diferentes)", fontweight="bold")
        ax2.set_xlabel("Generación")
        ax2.set_ylabel("Mejor Aptitud")
        ax2.set_xticks(range(0, 21, 2))
        ax2.set_ylim(400, 1020)
        ax2.legend(loc="lower right", fontsize=9)
        ax2.grid(True)

        plt.tight_layout()
        path = os.path.join(self.output_dir, "punto1_algoritmo_genetico.png")
        plt.savefig(path)
        plt.close()
        return path

    def plot_punto2_hill_climbing(self, values: List[int]) -> str:
        x_indices = list(range(len(values)))
        plt.figure(figsize=(10, 5.5))
        plt.plot(x_indices, values, color="#2b5c8f", linestyle="-", linewidth=2.5, zorder=1)
        plt.scatter(x_indices, values, color="#2b5c8f", s=80, zorder=2)

        plt.scatter([2], [7], color="#d9534f", s=160, zorder=3, label="Máximo Local (x=2, f=7)")
        plt.scatter([6], [9], color="#2ca02c", s=200, zorder=3, marker="*", label="Máximo Global (x=6, f=9)")

        for x, val in zip(x_indices, values):
            plt.annotate(f"f({x})={val}", (x, val), textcoords="offset points", xytext=(0, 10), ha="center", fontweight="bold")

        plt.axvspan(-0.5, 3.5, color="#f0ad4e", alpha=0.18, label="Cuenca Máximo Local (x ∈ [0, 3], 44.4%)")
        plt.axvspan(3.5, 8.5, color="#5cb85c", alpha=0.18, label="Cuenca Máximo Global (x ∈ [4, 8], 55.6%)")

        plt.title("Paisaje de Búsqueda y Cuencas de Atracción - Ascenso de Colinas", fontweight="bold")
        plt.xlabel("Estado Discreto $x$")
        plt.ylabel("Aptitud $f(x)$")
        plt.xticks(x_indices)
        plt.yticks(range(0, 11))
        plt.legend(loc="upper left")
        plt.grid(True)

        plt.tight_layout()
        path = os.path.join(self.output_dir, "punto2_ascenso_colinas.png")
        plt.savefig(path)
        plt.close()
        return path

    def plot_punto3_simulated_annealing(self, hist: Dict[str, List]) -> str:
        iters = hist["iteration"]
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.2))

        ax1.plot(iters, hist["current_energy"], color="#7f7f7f", alpha=0.6, linewidth=1.2, label="Energía Estado Actual $E(x_k)$")
        ax1.step(iters, hist["best_energy"], color="#1f77b4", linewidth=2.5, where="post", label="Mejor Energía Histórica $E^*$")
        ax1.axhline(0, color="crimson", linestyle=":", linewidth=1.8, label="Mínimo Global Óptimo ($E=0$)")
        ax1.set_title("Evolución de la Energía - Temple Simulado", fontweight="bold")
        ax1.set_xlabel("Iteración $k$")
        ax1.set_ylabel("Energía $E(x) = x^2$")
        ax1.legend(loc="upper right")
        ax1.grid(True)

        ax2.plot(iters, hist["temperature"], color="#d62728", linewidth=2.0)
        ax2.set_title("Programa de Enfriamiento Geométrico ($T_{k+1} = 0.90 T_k$)", fontweight="bold")
        ax2.set_xlabel("Iteración $k$")
        ax2.set_ylabel("Temperatura $T$ (Escala Logarítmica)")
        ax2.set_yscale("log")
        ax2.grid(True, which="both")

        plt.tight_layout()
        path = os.path.join(self.output_dir, "punto3_temple_simulado.png")
        plt.savefig(path)
        plt.close()
        return path

    def plot_punto4_ant_colony(self, hist: Dict[str, Any], frequencies: Dict[str, int], lengths: Dict[str, float]) -> str:
        iters = hist["iteration"]
        routes = ["A-B-Z", "A-C-Z", "A-D-Z"]
        colores = {"A-B-Z": "#2ca02c", "A-C-Z": "#1f77b4", "A-D-Z": "#d62728"}

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.2))

        for r in routes:
            ax1.plot(iters, hist["tau"][r], "o-", color=colores[r], label=f"Ruta {r} (L={int(lengths[r])})")
        ax1.set_title("Evolución de Feromonas por Ruta (Q=10, rho=0.2)", fontweight="bold")
        ax1.set_xlabel("Iteración")
        ax1.set_ylabel("Nivel de Feromona tau_r")
        ax1.legend(loc="upper left")
        ax1.grid(True)

        counts = [frequencies[r] for r in routes]
        total = sum(counts)
        porcentajes = [c / total * 100 for c in counts]
        barras = ax2.bar(routes, counts, color=[colores[r] for r in routes], edgecolor="black", width=0.55)
        for barra, pct in zip(barras, porcentajes):
            yval = barra.get_height()
            ax2.text(barra.get_x() + barra.get_width() / 2.0, yval + 3, f"{yval} ({pct:.1f}%)", ha="center", va="bottom", fontweight="bold")

        ax2.set_title("Frecuencia Total de Elección (200 Decisiones)", fontweight="bold")
        ax2.set_xlabel("Ruta")
        ax2.set_ylabel("Número de Hormigas")
        ax2.set_ylim(0, max(counts) + 25)
        ax2.grid(True, axis="y")

        plt.tight_layout()
        path = os.path.join(self.output_dir, "punto4_aco_hormigas.png")
        plt.savefig(path)
        plt.close()
        return path

    def plot_punto5_particle_swarm(self, hist_pos_list: List[np.ndarray], hist_fit: List[float], gbest: np.ndarray) -> str:
        hist_pos = np.array(hist_pos_list)
        iters = list(range(len(hist_fit)))

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

        grid_x = np.linspace(-5.2, 5.2, 200)
        grid_y = np.linspace(-5.2, 5.2, 200)
        X_grid, Y_grid = np.meshgrid(grid_x, grid_y)
        Z_grid = X_grid ** 2 + Y_grid ** 2

        cp = ax1.contourf(X_grid, Y_grid, Z_grid, levels=25, cmap="viridis", alpha=0.75)
        fig.colorbar(cp, ax=ax1, label="$f(x, y) = x^2 + y^2$")

        num_parts = hist_pos.shape[1]
        for p in range(num_parts):
            ax1.plot(hist_pos[:, p, 0], hist_pos[:, p, 1], ".-", alpha=0.55, linewidth=1.0)
            ax1.scatter(hist_pos[0, p, 0], hist_pos[0, p, 1], color="white", edgecolor="black", s=30, zorder=3)

        ax1.scatter(gbest[0], gbest[1], color="red", marker="*", s=260, zorder=5, label=f"Mejor Global ({gbest[0]:.4f}, {gbest[1]:.4f})")
        ax1.scatter(0, 0, color="gold", marker="x", s=140, linewidths=2.5, zorder=4, label="Óptimo Teórico (0, 0)")
        ax1.set_title("Convergencia del Enjambre en el Dominio $[-5, 5]^2$", fontweight="bold")
        ax1.set_xlabel("$x$")
        ax1.set_ylabel("$y$")
        ax1.set_xlim(-5.2, 5.2)
        ax1.set_ylim(-5.2, 5.2)
        ax1.legend(loc="upper right", framealpha=0.9)

        ax2.plot(iters, hist_fit, "o-", color="#1f77b4", linewidth=2.0)
        ax2.set_title("Convergencia de la Mejor Aptitud Global $f(g^{best})$", fontweight="bold")
        ax2.set_xlabel("Iteración")
        ax2.set_ylabel("Aptitud $f(x, y)$ (Escala Logarítmica)")
        ax2.set_yscale("log")
        ax2.grid(True, which="both")

        plt.tight_layout()
        path = os.path.join(self.output_dir, "punto5_pso_particulas.png")
        plt.savefig(path)
        plt.close()
        return path
