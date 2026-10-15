"""
Solucionador de Ascenso de Colinas (Punto 2).
Provee tanto la clase HillClimbingSolver como la función obligatoria ascenso_colinas().
"""

from typing import List, Optional, Tuple
from ..core.base import BaseOptimizer, OptimizationResult


class HillClimbingSolver(BaseOptimizer):
    """
    Optimizador de Ascenso de Colinas Discreto (Steepest Ascent con Mejora Estricta).
    """

    def __init__(
        self,
        values: Optional[List[int]] = None,
        start_index: int = 0,
        seed: Optional[int] = None,
    ):
        super().__init__(name="Ascenso de Colinas", seed=seed)
        self.values = values or [1, 4, 7, 5, 3, 6, 9, 8, 5]
        self.start_index = start_index
        self.current_index = start_index
        self.trajectory: List[int] = []
        self._terminated = False

    def _initialize(self) -> None:
        self.current_index = self.start_index
        self.trajectory = [self.current_index]
        self._terminated = False
        self._history = {"trajectory": self.trajectory}

    def _step(self, iteration: int) -> None:
        n = len(self.values)
        neighbors = []
        if self.current_index > 0:
            neighbors.append(self.current_index - 1)
        if self.current_index < n - 1:
            neighbors.append(self.current_index + 1)

        best_neighbor = max(neighbors, key=lambda v: self.values[v])

        if self.values[best_neighbor] > self.values[self.current_index]:
            self.current_index = best_neighbor
            self.trajectory.append(self.current_index)
        else:
            self._terminated = True

    def _is_terminated(self, iteration: int) -> bool:
        return self._terminated

    def _build_result(self, execution_time: float) -> OptimizationResult:
        final_val = self.values[self.current_index]
        return OptimizationResult(
            algorithm_name=self.name,
            best_solution=self.current_index,
            best_fitness=float(final_val),
            history={"trajectory": list(self.trajectory)},
            execution_time=execution_time,
            metadata={
                "start_index": self.start_index,
                "is_global_maximum": (self.current_index == 6),
                "final_value": final_val,
            },
        )


# ==============================================================================
# INTERFAZ OBLIGATORIA DEL PARCIAL (PDF)
# ==============================================================================

def ascenso_colinas(valores: List[int], inicio: int) -> Tuple[int, List[int]]:
    """
    Función requerida por el enunciado:
    def ascenso_colinas(valores, inicio):
        '''Devuelve el estado final y la trayectoria.'''
    """
    solver = HillClimbingSolver(values=valores, start_index=inicio)
    result = solver.solve()
    return result.best_solution, result.history["trajectory"]
