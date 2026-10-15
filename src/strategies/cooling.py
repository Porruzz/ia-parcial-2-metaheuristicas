"""
Estrategias de Enfriamiento Térmico (Patrón Strategy - GoF).
Desacopla el programa de enfriamiento de la lógica del Temple Simulado.
"""

from abc import ABC, abstractmethod


class CoolingSchedule(ABC):
    """Interfaz abstracta para el decaimiento térmico en Temple Simulado."""

    @abstractmethod
    def next_temperature(self, current_temp: float, iteration: int) -> float:
        """Calcula la temperatura de la siguiente iteración."""
        pass


class GeometricCoolingSchedule(CoolingSchedule):
    """
    Estrategia de Enfriamiento Geométrico:
    T_{k+1} = factor * T_k
    """

    def __init__(self, cooling_factor: float = 0.90):
        if not (0.0 < cooling_factor < 1.0):
            raise ValueError("El factor de enfriamiento debe estar en el intervalo (0, 1).")
        self.cooling_factor = cooling_factor

    def next_temperature(self, current_temp: float, iteration: int) -> float:
        return current_temp * self.cooling_factor
