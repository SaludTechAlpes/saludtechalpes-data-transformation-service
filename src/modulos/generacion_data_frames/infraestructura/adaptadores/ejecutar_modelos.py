from src.modulos.generacion_data_frames.dominio.puertos.ejecutar_modelos import PuertoEjecutarModelos
import random
import logging
import os
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdaptadorEjecutarModelosIA(PuertoEjecutarModelos):
    """
    Adaptador que simula la ejecución de Modelos IA y la generación de DataFrames.
    """
    MODALIDADES = ["Rayos X", "Resonancia Magnética", "Tomografía Computarizada", "Ultrasonido"]
    REGIONES_ANATOMICAS = ["Tórax", "Cerebro", "Abdomen", "Rodilla", "Columna Vertebral"]
    PATOLOGIAS = ["Normal", "Fractura", "Tumor", "Infección", "Inflamación", "Maligno", "Benigno"]

    def ejecutar_modelos(self) -> str:
        """
        Simula la ejecución de modelos IA y la generación de un DataFrame sin generar archivos reales.
        """
        ruta_parquet = self._simular_generacion_archivo_parquet()

        return ruta_parquet
        
    def _simular_generacion_archivo_parquet(self) -> str:
        """
        Simula la generación de un archivo Parquet devolviendo solo la ruta.
        """
        directorio = "/simulacion/parquets"
        return f"{directorio}/dataframe_{random.randint(1000, 9999)}.parquet"
