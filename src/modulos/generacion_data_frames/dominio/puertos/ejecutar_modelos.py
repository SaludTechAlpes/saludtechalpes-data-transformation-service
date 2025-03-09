from abc import ABC, abstractmethod

class PuertoEjecutarModelos(ABC):
    """
    Puerto de dominio para procesar el comando `Ejecutar Pipelines y Modelos`.
    """
    @abstractmethod
    def ejecutar_modelos(self) -> str:
        """
        Procesa la ejecución de modelos IA.
        """
        ...