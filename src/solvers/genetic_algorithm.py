"""
Solucionador de Algoritmo Genético (Punto 1).
Integra las estrategias de selección, cruce y mutación (Inyección de Dependencias).
"""

import random
from typing import Callable, List, Optional
import numpy as np

from ..core.base import BaseOptimizer, OptimizationResult
from ..strategies.genetic import (
    BitFlipMutation,
    CrossoverStrategy,
    MutationStrategy,
    RouletteWheelSelection,
    SelectionStrategy,
    SinglePointCrossover,
)


class GeneticAlgorithmSolver(BaseOptimizer):
    """
    Optimizador Genético Canónico con Elitismo y Operadores Modulares.
    """

    def __init__(
        self,
        fitness_function: Optional[Callable[[int], float]] = None,
        initial_population: Optional[List[str]] = None,
        generations: int = 20,
        crossover_rate: float = 0.80,
        mutation_rate: float = 0.05,
        selection_strategy: Optional[SelectionStrategy] = None,
        crossover_strategy: Optional[CrossoverStrategy] = None,
        mutation_strategy: Optional[MutationStrategy] = None,
        seed: Optional[int] = 42,
    ):
        super().__init__(name="Algoritmo Genético", seed=seed)
        self.fitness_func = fitness_function or (lambda x: float(x ** 2))
        self.initial_population = initial_population or ["00101", "01100", "10010", "11001"]
        self.generations = generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate

        # Inyección de Estrategias GoF
        self.selection_strategy = selection_strategy or RouletteWheelSelection()
        self.crossover_strategy = crossover_strategy or SinglePointCrossover()
        self.mutation_strategy = mutation_strategy or BitFlipMutation()

        self.population: List[str] = []
        self.chromosome_length: int = 5
        self.pop_size: int = 4

    def _decode(self, chromosome: str) -> int:
        return int(chromosome, 2)

    def _initialize(self) -> None:
        if self.seed is not None:
            random.seed(self.seed)
            np.random.seed(self.seed)

        self.population = list(self.initial_population)
        self.pop_size = len(self.population)
        self.chromosome_length = len(self.population[0])

        self._history = {
            "generation": [],
            "best_fitness": [],
            "average_fitness": [],
            "best_x": [],
            "best_chromosome": [],
        }

    def _step(self, iteration: int) -> None:
        decoded_values = [self._decode(chrom) for chrom in self.population]
        fitnesses = [self.fitness_func(x) for x in decoded_values]

        best_idx = int(np.argmax(fitnesses))
        best_chrom = self.population[best_idx]
        best_x = decoded_values[best_idx]
        best_fit = fitnesses[best_idx]
        avg_fit = float(np.mean(fitnesses))

        # Registro histórico
        self._history["generation"].append(iteration)
        self._history["best_fitness"].append(best_fit)
        self._history["average_fitness"].append(avg_fit)
        self._history["best_x"].append(best_x)
        self._history["best_chromosome"].append(best_chrom)

        if iteration == self.generations:
            return

        # 1. Elitismo: Preservar al mejor individuo de la generación
        new_population = [best_chrom]

        # 2. Generación del resto de la descendencia usando las estrategias
        while len(new_population) < self.pop_size:
            parents = self.selection_strategy.select(self.population, fitnesses, k=2)
            c1, c2 = self.crossover_strategy.cross(parents[0], parents[1], self.crossover_rate)
            c1 = self.mutation_strategy.mutate(c1, self.mutation_rate)
            c2 = self.mutation_strategy.mutate(c2, self.mutation_rate)

            new_population.append(c1)
            if len(new_population) < self.pop_size:
                new_population.append(c2)

        self.population = new_population

    def _is_terminated(self, iteration: int) -> bool:
        return iteration > self.generations

    def _build_result(self, execution_time: float) -> OptimizationResult:
        return OptimizationResult(
            algorithm_name=self.name,
            best_solution=self._history["best_chromosome"][-1],
            best_fitness=self._history["best_fitness"][-1],
            history=self._history,
            execution_time=execution_time,
            metadata={
                "best_decimal_x": self._history["best_x"][-1],
                "generations": self.generations,
                "crossover_rate": self.crossover_rate,
                "mutation_rate": self.mutation_rate,
                "seed": self.seed,
            },
        )
