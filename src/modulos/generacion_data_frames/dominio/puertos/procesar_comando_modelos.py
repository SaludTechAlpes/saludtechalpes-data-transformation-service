from abc import ABC, abstractmethod

class PuertoProcesarComandoModelos(ABC):
    """
    Puerto de dominio para procesar el comando `Ejecutar Pipelines y Modelos`.
    """
    @abstractmethod
    def procesar_comando_ejecutar_modelos(self, id_imagen_importada:str, id_imagen_anonimizada:str, id_imagen_mapeada:str, cluster_id: str, ruta_imagen_anonimizada: str, evento_a_fallar: str) -> str:
        """
        Procesa el comando de ejecución de modelos IA.
        """
        ...

    @abstractmethod
    def procesar_comando_revertir_ejecucion(self, id_dataframe: str) -> str:
        ...