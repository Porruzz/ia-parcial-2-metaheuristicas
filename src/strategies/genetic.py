"""
Estrategias de Operadores Genéticos (Patrón Strategy - GoF).
Permite desacoplar y hacer intercambiables los mecanismos de Selección, Cruce y Mutación.
"""

import random
from abc import ABC, abstractmethod
from typing import List, Tuple


# ==============================================================================
# ESTRATEGIAS DE SELECCIÓN
# ==============================================================================

class SelectionStrategy(ABC):
    """Interfaz abstracta para la estrategia de selección de parentales."""

    @abstractmethod
    def select(self, population: List[str], fitnesses: List[float], k: int = 2) -> List[str]:
        """Selecciona k individuos de la población según sus aptitudes."""
        pass


class RouletteWheelSelection(SelectionStrategy):
    """
    Estrategia de Selección Proporcional a la Aptitud (Ruleta de Montecarlo).
    p_i = f(x_i) / sum(f(x_j))
    """

    def select(self, population: List[str], fitnesses: List[float], k: int = 2) -> List[str]:
        total_fitness = sum(fitnesses)
        if total_fitness <= 0:
            return random.choices(population, k=k)
        probabilities = [f / total_fitness for f in fitnesses]
        return random.choices(population, weights=probabilities, k=k)


# ==============================================================================
# ESTRATEGIAS DE CRUCE (RECOMBINACIÓN)
# ==============================================================================

class CrossoverStrategy(ABC):
    """Interfaz abstracta para la estrategia de cruce o recombinación."""

    @abstractmethod
    def cross(self, parent1: str, parent2: str, crossover_rate: float) -> Tuple[str, str]:
        """Aplica el operador de cruce entre dos padres con una probabilidad dada."""
        pass


class SinglePointCrossover(CrossoverStrategy):
    """
    Estrategia de Cruce de un Punto:
    Con probabilidad crossover_rate, selecciona un punto de corte aleatorio
    e intercambia los segmentos de ambos cromosomas.
    """

    def cross(self, parent1: str, parent2: str, crossover_rate: float) -> Tuple[str, str]:
        if random.random() < crossover_rate and len(parent1) > 1:
            point = random.randint(1, len(parent1) - 1)
            child1 = parent1[:point] + parent2[point:]
            child2 = parent2[:point] + parent1[point:]
            return child1, child2
        return parent1, parent2


# ==============================================================================
# ESTRATEGIAS DE MUTACIÓN
# ==============================================================================

class MutationStrategy(ABC):
    """Interfaz abstracta para la estrategia de mutación genética."""

    @abstractmethod
    def mutate(self, chromosome: str, mutation_rate: float) -> str:
        """Aplica mutación estocástica a un cromosoma."""
        pass


class BitFlipMutation(MutationStrategy):
    """
    Estrategia de Mutación Bit-Flip Independiente:
    Cada bit se invierte de 0 a 1 o de 1 a 0 con probabilidad mutation_rate.
    """

    def mutate(self, chromosome: str, mutation_rate: float) -> str:
        bits = list(chromosome)
        for i in range(len(bits)):
            if random.random() < mutation_rate:
                bits[i] = "1" if bits[i] == "0" else "0"
        return "".join(bits)
