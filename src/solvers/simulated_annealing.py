"""
Solucionador de Temple Simulado (Punto 3).
Utiliza el Patrón Strategy para el programa de enfriamiento térmico.
"""

import math
import random
from typing import Callable, List, Optional

from ..core.base import BaseOptimizer, OptimizationResult
from ..strategies.cooling import CoolingSchedule, GeometricCoolingSchedule


class SimulatedAnnealingSolver(BaseOptimizer):
    """
    Optimizador de Temple Simulado (Metrópolis) para minimización de energía.
    """

    def __init__(
        self,
        energy_function: Optional[Callable[[int], float]] = None,
        x0: int = 5,
        t0: float = 10.0,
        max_iterations: int = 100,
        domain_bounds: tuple = (-5, 5),
        cooling_schedule: Optional[CoolingSchedule] = None,
        seed: Optional[int] = 42,
    ):
        super().__init__(name="Temple Simulado", seed=seed)
        self.energy_func = energy_function or (lambda x: float(x ** 2))
        self.x0 = x0
        self.t0 = t0
        self.max_iterations = max_iterations
        self.domain_bounds = domain_bounds
        self.cooling_schedule = cooling_schedule or GeometricCoolingSchedule(cooling_factor=0.90)

        self.current_x = x0
        self.current_e = 0.0
        self.best_x = x0
        self.best_e = 0.0
        self.temperature = t0

    def _initialize(self) -> None:
        if self.seed is not None:
            random.seed(self.seed)

        self.current_x = self.x0
        self.current_e = self.energy_func(self.current_x)
        self.best_x = self.current_x
        self.best_e = self.current_e
        self.temperature = self.t0

        self._history = {
            "iteration": [],
            "temperature": [],
            "current_x": [],
            "current_energy": [],
            "best_x": [],
            "best_energy": [],
        }

    def _step(self, iteration: int) -> None:
        # Registro antes de la transición
        self._history["iteration"].append(iteration)
        self._history["temperature"].append(self.temperature)
        self._history["current_x"].append(self.current_x)
        self._history["current_energy"].append(self.current_e)
        self._history["best_x"].append(self.best_x)
        self._history["best_energy"].append(self.best_e)

        # Generar vecinos válidos en el dominio
        neighbors: List[int] = []
        if self.current_x > self.domain_bounds[0]:
            neighbors.append(self.current_x - 1)
        if self.current_x < self.domain_bounds[1]:
            neighbors.append(self.current_x + 1)

        candidate_x = random.choice(neighbors)
        candidate_e = self.energy_func(candidate_x)
        delta_e = candidate_e - self.current_e

        # Criterio de Metrópolis
        if delta_e <= 0:
            accept = True
        else:
            p_accept = math.exp(-delta_e / self.temperature)
            u = random.random()
            accept = (u < p_accept)

        if accept:
            self.current_x = candidate_x
            self.current_e = candidate_e
            if self.current_e < self.best_e:
                self.best_x = self.current_x
                self.best_e = self.current_e

        # Actualizar temperatura según la estrategia inyectada
        self.temperature = self.cooling_schedule.next_temperature(self.temperature, iteration)

    def _is_terminated(self, iteration: int) -> bool:
        return iteration >= self.max_iterations

    def _build_result(self, execution_time: float) -> OptimizationResult:
        return OptimizationResult(
            algorithm_name=self.name,
            best_solution=self.best_x,
            best_fitness=self.best_e,
            history=self._history,
            execution_time=execution_time,
            metadata={
                "final_x": self.current_x,
                "final_energy": self.current_e,
                "final_temperature": self.temperature,
                "max_iterations": self.max_iterations,
                "seed": self.seed,
            },
        )
