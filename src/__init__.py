"""
Paquete principal de Metaheurísticas e Inteligencia Artificial (2026).
Arquitectura orientada a objetos con patrones de diseño GoF:
- Template Method (BaseOptimizer)
- Strategy Pattern (Selection, Crossover, Mutation, Cooling)
- Factory Method / Registry Pattern (OptimizerFactory)
- Value Object Pattern (OptimizationResult)
"""

from .core.base import BaseOptimizer, OptimizationResult
from .solvers import (
    GeneticAlgorithmSolver,
    HillClimbingSolver,
    ascenso_colinas,
    SimulatedAnnealingSolver,
    AntColonySolver,
    ParticleSwarmSolver,
    OptimizerFactory,
)
from .utils.visualizer import ParcialVisualizer

__all__ = [
    "BaseOptimizer",
    "OptimizationResult",
    "GeneticAlgorithmSolver",
    "HillClimbingSolver",
    "ascenso_colinas",
    "SimulatedAnnealingSolver",
    "AntColonySolver",
    "ParticleSwarmSolver",
    "OptimizerFactory",
    "ParcialVisualizer",
]
