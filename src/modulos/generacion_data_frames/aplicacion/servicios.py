from src.modulos.generacion_data_frames.dominio.puertos.procesar_comando_modelos import PuertoProcesarComandoModelos
from src.modulos.generacion_data_frames.dominio.puertos.ejecutar_modelos import PuertoEjecutarModelos
from src.modulos.generacion_data_frames.dominio.entidades import DataFrame
from src.modulos.generacion_data_frames.dominio.puertos.repositorios import RepositorioDataFrame
from src.modulos.generacion_data_frames.infraestructura.despachadores import Despachador
from src.modulos.generacion_data_frames.dominio.eventos import DataFramesGeneradosEvento, DataFramesGeneradosFallidoEvento
from datetime import datetime, timezone
import logging
import uuid


# Configuración de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ServicioAplicacionGeneracionDataFrames(PuertoProcesarComandoModelos):
    def __init__(self, adaptador_modelos: PuertoEjecutarModelos, repositorio_dataframes: RepositorioDataFrame):
        self.adaptador_modelos = adaptador_modelos
        self.repositorio_dataframes = repositorio_dataframes
        self.despachador = Despachador()

    def procesar_comando_ejecutar_modelos(self, id_imagen_importada:str, id_imagen_anonimizada:str, id_imagen_mapeada:str, cluster_id: str, ruta_imagen_anonimizada: str, evento_a_fallar: str):
        id_dataframe = uuid.uuid4()
        try:
            ruta_parquet = self.adaptador_modelos.ejecutar_modelos()

            if not ruta_parquet:
                raise ValueError("Error: No se pudo generar el archivo Parquet")

            dataframe = DataFrame(
                id=id_dataframe,
                cluster_id=cluster_id,
                ruta_archivo_parquet=ruta_parquet,
                fecha_generacion=datetime.now(timezone.utc)
            )

            self.repositorio_dataframes.agregar(dataframe)

            if evento_a_fallar == 'DataFramesGenerados':
                raise ValueError("Error: Error al generar dataframe")

            evento = DataFramesGeneradosEvento(
                id_dataframe=str(dataframe.id),
                cluster_id=cluster_id,
                ruta_archivo_parquet=ruta_parquet,
                fecha_generacion=dataframe.fecha_generacion,
                evento_a_fallar=evento_a_fallar
            )

            self.despachador.publicar_evento(evento, "dataframes-generados")

            logger.info(f"👉 DataFrame {dataframe.id} almacenado y evento publicado en `dataframes-generados`: {evento}")

        except Exception as e:
            evento = DataFramesGeneradosFallidoEvento(
                id_imagen_mapeada=id_imagen_mapeada,
                id_imagen_anonimizada=id_imagen_anonimizada,
                id_imagen_importada=id_imagen_importada,
                id_dataframe=id_dataframe
            )

            self.despachador.publicar_evento_fallido(evento, 'generacion-dataframes-fallido')
            logger.error(f"❌ Error al mapear la imagen y evento publicado al topico generacion-dataframes-fallido: {e}")
            raise

    def procesar_comando_revertir_ejecucion(self, id_dataframe: str):
        try:
            dataframe = self.repositorio_dataframes.obtener_por_id(id_dataframe)

            if dataframe:
                self.repositorio_dataframes.eliminar(dataframe.id)

                logger.info(f"🔄 Reversión ejecutada: Dataframe {dataframe} eliminado.")
            else:
                logger.warning(f"⚠️ No se encontró el dataframe {id_dataframe}, no hay nada que eliminar.")

        except Exception as e:
            logger.error(f"❌ Error al revertir la generación del dataframe {id_dataframe}: {e}")
            raise