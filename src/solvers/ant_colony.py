"""
Solucionador de Optimización por Colonia de Hormigas - ACO (Punto 4).
Modela la toma de decisiones estigmergica y la evaporación/depósito de feromonas.
"""

import random
from typing import Dict, List, Optional
import numpy as np

from ..core.base import BaseOptimizer, OptimizationResult


class AntColonySolver(BaseOptimizer):
    """
    Optimizador ACO simplificado para selección de rutas discretas.
    """

    def __init__(
        self,
        routes: Optional[List[str]] = None,
        lengths: Optional[Dict[str, float]] = None,
        num_ants: int = 10,
        iterations: int = 20,
        alpha: float = 1.0,
        beta: float = 2.0,
        rho: float = 0.20,
        q: float = 10.0,
        seed: Optional[int] = 42,
    ):
        super().__init__(name="Colonia de Hormigas (ACO)", seed=seed)
        self.routes = routes or ["A-B-Z", "A-C-Z", "A-D-Z"]
        self.lengths = lengths or {"A-B-Z": 6.0, "A-C-Z": 8.0, "A-D-Z": 10.0}
        self.num_ants = num_ants
        self.iterations = iterations
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.q = q

        self.tau: Dict[str, float] = {}
        self.selection_counts: Dict[str, int] = {}

    def _initialize(self) -> None:
        if self.seed is not None:
            random.seed(self.seed)
            np.random.seed(self.seed)

        self.tau = {r: 1.0 for r in self.routes}
        self.selection_counts = {r: 0 for r in self.routes}

        self._history = {
            "iteration": [],
            "tau": {r: [] for r in self.routes},
            "probabilities": {r: [] for r in self.routes},
            "iteration_counts": {r: [] for r in self.routes},
        }

    def _step(self, iteration: int) -> None:
        # 1. Calcular probabilidades de transición
        weights = {
            r: (self.tau[r] ** self.alpha) * ((1.0 / self.lengths[r]) ** self.beta)
            for r in self.routes
        }
        sum_weights = sum(weights.values())
        probs = {r: weights[r] / sum_weights for r in self.routes}

        # Guardar historial
        self._history["iteration"].append(iteration)
        for r in self.routes:
            self._history["tau"][r].append(self.tau[r])
            self._history["probabilities"][r].append(probs[r])

        # 2. Las hormigas eligen rutas estocásticamente
        prob_list = [probs[r] for r in self.routes]
        choices = random.choices(self.routes, weights=prob_list, k=self.num_ants)

        iter_counts = {r: choices.count(r) for r in self.routes}
        for r in self.routes:
            self.selection_counts[r] += iter_counts[r]
            self._history["iteration_counts"][r].append(iter_counts[r])

        # 3. Evaporación de feromona
        for r in self.routes:
            self.tau[r] = (1.0 - self.rho) * self.tau[r]

        # 4. Depósito de feromona por hormigas que atravesaron la ruta
        for r in self.routes:
            self.tau[r] += iter_counts[r] * (self.q / self.lengths[r])

    def _is_terminated(self, iteration: int) -> bool:
        return iteration >= self.iterations

    def _build_result(self, execution_time: float) -> OptimizationResult:
        best_route = min(self.routes, key=lambda r: self.lengths[r])
        return OptimizationResult(
            algorithm_name=self.name,
            best_solution=best_route,
            best_fitness=self.lengths[best_route],
            history=self._history,
            execution_time=execution_time,
            metadata={
                "selection_frequencies": dict(self.selection_counts),
                "final_pheromones": dict(self.tau),
                "total_decisions": self.num_ants * self.iterations,
                "lengths": dict(self.lengths),
                "seed": self.seed,
            },
        )
