from src.modulos.generacion_data_frames.dominio.puertos.procesar_comando_modelos import PuertoProcesarComandoModelos
from src.modulos.generacion_data_frames.infraestructura.adaptadores.ejecutar_modelos import AdaptadorEjecutarModelosIA
from src.modulos.generacion_data_frames.dominio.entidades import DataFrame
from src.modulos.generacion_data_frames.dominio.puertos.repositorios import RepositorioDataFrame
from src.modulos.generacion_data_frames.infraestructura.despachadores import DespachadorGeneracionDataFrames
from src.modulos.generacion_data_frames.dominio.eventos import DataFramesGeneradosEvento
import uuid
from datetime import datetime, timezone
import logging

# Configuración de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ServicioAplicacionGeneracionDataFrames(PuertoProcesarComandoModelos):
    """
    Servicio de Aplicación que gestiona la generación de DataFrames.
    """
    def __init__(self, adaptador_modelos: AdaptadorEjecutarModelosIA, repositorio_dataframes: RepositorioDataFrame):
        self.adaptador_modelos = adaptador_modelos
        self.repositorio_dataframes = repositorio_dataframes
        self.despachador = DespachadorGeneracionDataFrames()

    def procesar_comando_ejecutar_modelos(self, cluster_id: str, ruta_imagen_anonimizada: str):
        """
        Orquesta el flujo de generación del DataFrame y su almacenamiento.
        """
        try:
            ruta_parquet = self.adaptador_modelos.procesar_comando_ejecutar_modelos(cluster_id, ruta_imagen_anonimizada)

            if not ruta_parquet:
                raise ValueError("Error: No se pudo generar el archivo Parquet")

            logger.info(f"Archivo Parquet generado: {ruta_parquet}")

            dataframe = DataFrame(
                id=uuid.uuid4(),
                cluster_id=cluster_id,
                ruta_archivo_parquet=ruta_parquet,
                fecha_generacion=datetime.now(timezone.utc)
            )

            self.repositorio_dataframes.agregar(dataframe)

            evento = DataFramesGeneradosEvento(
                id=str(dataframe.id),
                cluster_id=cluster_id,
                ruta_archivo_parquet=ruta_parquet,
                fecha_generacion=dataframe.fecha_generacion.isoformat()
            )

            self.despachador.publicar_evento(evento, "dataframes-generados")

            logger.info(f"DataFrame {dataframe.id} almacenado y evento publicado en `dataframes-generados`: {evento}")

        except Exception as e:
            logger.error(f"Error al generar el DataFrame: {e}")
            raise
