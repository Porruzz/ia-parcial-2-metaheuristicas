"""
Fábrica de Optimizadores (Patrón Factory Method / Registry - GoF).
Desacopla la creación de instancias concretas de optimizadores del cliente.
"""

from typing import Any, Dict, Type
from ..core.base import BaseOptimizer
from .genetic_algorithm import GeneticAlgorithmSolver
from .hill_climbing import HillClimbingSolver
from .simulated_annealing import SimulatedAnnealingSolver
from .ant_colony import AntColonySolver
from .particle_swarm import ParticleSwarmSolver


class OptimizerFactory:
    """
    Fábrica estática y registro para instanciación de metaheurísticas.
    """

    _registry: Dict[str, Type[BaseOptimizer]] = {
        "ga": GeneticAlgorithmSolver,
        "genetic": GeneticAlgorithmSolver,
        "hc": HillClimbingSolver,
        "hill_climbing": HillClimbingSolver,
        "sa": SimulatedAnnealingSolver,
        "simulated_annealing": SimulatedAnnealingSolver,
        "aco": AntColonySolver,
        "ant_colony": AntColonySolver,
        "pso": ParticleSwarmSolver,
        "particle_swarm": ParticleSwarmSolver,
    }

    @classmethod
    def register(cls, name: str, solver_class: Type[BaseOptimizer]) -> None:
        """Permite extender la fábrica en tiempo de ejecución (Open/Closed Principle)."""
        cls._registry[name.lower()] = solver_class

    @classmethod
    def create(cls, optimizer_type: str, **kwargs: Any) -> BaseOptimizer:
        """
        Crea una instancia configurada del optimizador solicitado.
        """
        key = optimizer_type.lower()
        if key not in cls._registry:
            valid_keys = ", ".join(sorted(cls._registry.keys()))
            raise ValueError(f"Optimizador '{optimizer_type}' no registrado. Disponibles: {valid_keys}")

        solver_cls = cls._registry[key]
        return solver_cls(**kwargs)
