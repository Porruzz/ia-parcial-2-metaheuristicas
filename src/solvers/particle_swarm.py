"""
Solucionador de Optimización por Enjambre de Partículas - PSO (Punto 5).
Modela la dinámica de bandadas con inercia, componente cognitivo y social en 2D.
"""

from typing import Callable, Optional, Tuple
import numpy as np

from ..core.base import BaseOptimizer, OptimizationResult


class ParticleSwarmSolver(BaseOptimizer):
    """
    Optimizador PSO Canónico con Fronteras Absorbentes y Actualización Sincrónica.
    """

    def __init__(
        self,
        objective_function: Optional[Callable[[np.ndarray], np.ndarray]] = None,
        num_particles: int = 10,
        dimension: int = 2,
        iterations: int = 30,
        w: float = 0.50,
        c1: float = 1.50,
        c2: float = 1.50,
        bounds: Tuple[float, float] = (-5.0, 5.0),
        seed: Optional[int] = 42,
    ):
        super().__init__(name="Enjambre de Partículas (PSO)", seed=seed)
        self.objective_func = objective_function or (lambda pos: np.sum(pos ** 2, axis=-1))
        self.num_particles = num_particles
        self.dim = dimension
        self.iterations = iterations
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.bounds = bounds

        self.X: np.ndarray = np.empty((0, 0))
        self.V: np.ndarray = np.empty((0, 0))
        self.pbest_X: np.ndarray = np.empty((0, 0))
        self.pbest_fitness: np.ndarray = np.empty(0)
        self.gbest_X: np.ndarray = np.empty(0)
        self.gbest_fitness: float = float("inf")

    def _initialize(self) -> None:
        if self.seed is not None:
            np.random.seed(self.seed)

        self.X = np.random.uniform(self.bounds[0], self.bounds[1], (self.num_particles, self.dim))
        self.V = np.zeros((self.num_particles, self.dim))

        self.pbest_X = np.copy(self.X)
        self.pbest_fitness = self.objective_func(self.pbest_X)

        best_idx = int(np.argmin(self.pbest_fitness))
        self.gbest_X = np.copy(self.pbest_X[best_idx])
        self.gbest_fitness = float(self.pbest_fitness[best_idx])

        self._history = {
            "gbest_fitness": [self.gbest_fitness],
            "gbest_position": [self.gbest_X.copy()],
            "swarm_positions": [self.X.copy()],
        }

    def _step(self, iteration: int) -> None:
        # r1, r2 independientes por partícula y dimensión
        r1 = np.random.uniform(0.0, 1.0, (self.num_particles, self.dim))
        r2 = np.random.uniform(0.0, 1.0, (self.num_particles, self.dim))

        # Actualización sincrónica: usar el mismo gbest para toda la iteración
        v_new = (
            self.w * self.V
            + self.c1 * r1 * (self.pbest_X - self.X)
            + self.c2 * r2 * (self.gbest_X - self.X)
        )
        x_new = self.X + v_new

        # Manejo de fronteras: ajustar al límite y anular velocidad si excede
        for i in range(self.num_particles):
            for d in range(self.dim):
                if x_new[i, d] < self.bounds[0]:
                    x_new[i, d] = self.bounds[0]
                    v_new[i, d] = 0.0
                elif x_new[i, d] > self.bounds[1]:
                    x_new[i, d] = self.bounds[1]
                    v_new[i, d] = 0.0

        self.X = x_new
        self.V = v_new

        # Evaluación y actualización de memorias
        current_fits = self.objective_func(self.X)
        for i in range(self.num_particles):
            if current_fits[i] < self.pbest_fitness[i]:
                self.pbest_fitness[i] = current_fits[i]
                self.pbest_X[i] = np.copy(self.X[i])

        iter_best_idx = int(np.argmin(self.pbest_fitness))
        if self.pbest_fitness[iter_best_idx] < self.gbest_fitness:
            self.gbest_fitness = float(self.pbest_fitness[iter_best_idx])
            self.gbest_X = np.copy(self.pbest_X[iter_best_idx])

        self._history["gbest_fitness"].append(self.gbest_fitness)
        self._history["gbest_position"].append(self.gbest_X.copy())
        self._history["swarm_positions"].append(self.X.copy())

    def _is_terminated(self, iteration: int) -> bool:
        return iteration >= self.iterations

    def _build_result(self, execution_time: float) -> OptimizationResult:
        return OptimizationResult(
            algorithm_name=self.name,
            best_solution=self.gbest_X,
            best_fitness=self.gbest_fitness,
            history=self._history,
            execution_time=execution_time,
            metadata={
                "num_particles": self.num_particles,
                "dimension": self.dim,
                "iterations": self.iterations,
                "w": self.w,
                "c1": self.c1,
                "c2": self.c2,
                "bounds": self.bounds,
                "seed": self.seed,
            },
        )
