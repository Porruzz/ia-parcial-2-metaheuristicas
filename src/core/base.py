"""
Módulo Core: Abstracciones y Contratos Base para Metaheurísticas.
Aplica el Patrón Template Method y Value Object.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class OptimizationResult:
    """
    Value Object inmutable que encapsula el resultado de cualquier optimizador.
    """
    algorithm_name: str
    best_solution: Any
    best_fitness: float
    history: Dict[str, List[Any]] = field(default_factory=dict)
    execution_time: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseOptimizer(ABC):
    """
    Clase Base Abstracta para todos los optimizadores.
    Implementa el Patrón de Diseño Template Method (GoF):
    Define el esqueleto del algoritmo en `solve()`, delegando pasos específicos
    a las subclases concretas.
    """

    def __init__(self, name: str, seed: Optional[int] = 42):
        self.name = name
        self.seed = seed
        self._history: Dict[str, List[Any]] = {}

    @abstractmethod
    def _initialize(self) -> None:
        """Inicializa el estado interno del optimizador."""
        pass

    @abstractmethod
    def _step(self, iteration: int) -> None:
        """Ejecuta una iteración o generación individual del proceso de búsqueda."""
        pass

    @abstractmethod
    def _is_terminated(self, iteration: int) -> bool:
        """Verifica la condición de parada del algoritmo."""
        pass

    @abstractmethod
    def _build_result(self, execution_time: float) -> OptimizationResult:
        """Construye y retorna el Value Object con el resultado consolidado."""
        pass

    def solve(self) -> OptimizationResult:
        """
        Template Method principal. Coordina el ciclo de vida de la optimización:
        1. Inicialización
        2. Bucle iterativo de búsqueda
        3. Empaquetado inmutable del resultado
        """
        import time

        start_time = time.perf_counter()
        self._initialize()

        iteration = 0
        while not self._is_terminated(iteration):
            self._step(iteration)
            iteration += 1

        elapsed = time.perf_counter() - start_time
        return self._build_result(elapsed)
