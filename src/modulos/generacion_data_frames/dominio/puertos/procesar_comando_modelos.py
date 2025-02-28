from abc import ABC, abstractmethod

class PuertoProcesarComandoModelos(ABC):
    """
    Puerto de dominio para procesar el comando `Ejecutar Pipelines y Modelos`.
    """
    @abstractmethod
    def procesar_comando_ejecutar_modelos(self, cluster_id: str, ruta_imagen_anonimizada: str):
        """
        Procesa el comando de ejecución de modelos IA.
        """
        ...
