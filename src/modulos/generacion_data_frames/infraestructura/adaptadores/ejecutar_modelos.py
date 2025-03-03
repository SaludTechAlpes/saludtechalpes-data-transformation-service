from src.modulos.generacion_data_frames.dominio.puertos.procesar_comando_modelos import PuertoProcesarComandoModelos
import random
import logging
import os
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdaptadorEjecutarModelosIA(PuertoProcesarComandoModelos):
    """
    Adaptador que simula la ejecución de Modelos IA y la generación de DataFrames.
    """
    MODALIDADES = ["Rayos X", "Resonancia Magnética", "Tomografía Computarizada", "Ultrasonido"]
    REGIONES_ANATOMICAS = ["Tórax", "Cerebro", "Abdomen", "Rodilla", "Columna Vertebral"]
    PATOLOGIAS = ["Normal", "Fractura", "Tumor", "Infección", "Inflamación", "Maligno", "Benigno"]

    def procesar_comando_ejecutar_modelos(self, cluster_id: str, ruta_imagen_anonimizada: str) -> str:
        """
        Simula la ejecución de modelos IA y la generación de un DataFrame sin generar archivos reales.
        """
        ruta_parquet = self._simular_generacion_archivo_parquet()

        logger.info(f"Modelos IA ejecutados para cluster {cluster_id}. Simulación de archivo Parquet generado: {ruta_parquet}")

        return ruta_parquet

    def _simular_generacion_archivo_parquet(self) -> str:
        """
        Simula la generación de un archivo Parquet devolviendo solo la ruta.
        """
        directorio = "/simulacion/parquets"
        return f"{directorio}/dataframe_{random.randint(1000, 9999)}.parquet"
