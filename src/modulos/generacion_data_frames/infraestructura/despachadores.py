import pulsar
from pulsar.schema import AvroSchema
import logging
from src.modulos.generacion_data_frames.infraestructura.schema.v1.eventos import DataFramesGeneradosPayload, EventoDataFramesGenerados, DataFramesGeneradosFallidoPayload, EventoDataFramesGeneradosFallido
from src.modulos.generacion_data_frames.infraestructura.schema.v1.comandos import ComandoEjecutarModelosPayload, ComandoEjecutarModelos, ComandoRevertirEjecucionModelos, ComandoRevertirEjecucionModelosPayload
from src.modulos.generacion_data_frames.dominio.eventos import DataFramesGeneradosEvento, DataFramesGeneradosFallidoEvento
from src.config.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
config = Config()

class Despachador:
    """
    Despachador para publicar comandos y eventos en Apache Pulsar.
    """

    def _publicar_mensaje(self, mensaje, topico, schema):
        try:
            cliente = pulsar.Client(f'{config.PULSAR_HOST}://{config.BROKER_HOST}:6650')
            logger.info(f"📤 Publicando mensaje en {topico}: {mensaje.data}")
            publicador = cliente.create_producer(topico, schema=AvroSchema(schema))
            publicador.send(mensaje)
            logger.info(f"✅ Mensaje publicado con éxito en {topico}")
            cliente.close()
        except Exception as e:
            logger.error(f"❌ Error publicando mensaje en {topico}: {e}")

    
    def publicar_evento(self, evento, topico):
        payload = DataFramesGeneradosPayload(
                id=str(evento.id),
                id_dataframe=str(evento.id_dataframe),
                cluster_id=str(evento.cluster_id),
                ruta_archivo_parquet=evento.ruta_archivo_parquet,
                fecha_generacion=evento.fecha_generacion.isoformat(),
                evento_a_fallar=evento.evento_a_fallar
            )
        return EventoDataFramesGenerados(data=payload), EventoDataFramesGenerados


    def publicar_evento_fallido(self, evento, topico):
        payload = DataFramesGeneradosFallidoPayload(
            id_imagen_importada=str(evento.id_imagen_importada),
            id_imagen_anonimizada=str(evento.id_imagen_anonimizada),
            id_imagen_mapeada=str(evento.id_imagen_mapeada),
            id_dataframe=str(evento.id_dataframe)
        )
        evento_gordo=EventoDataFramesGeneradosFallido(data=payload)
        self._publicar_mensaje(evento_gordo, topico, EventoDataFramesGeneradosFallido)


    def publicar_comando(self, comando, topico):
        payload = ComandoEjecutarModelosPayload(
            id_imagen_importada=str(comando.id_imagen_importada), 
            id_imagen_anonimizada=str(comando.id_imagen_anonimizada), 
            id_imagen_mapeada=str(comando.id_imagen_mapeada), 
            cluster_id=str(comando.cluster_id),
            ruta_imagen_anonimizada=comando.ruta_imagen_anonimizada,
            evento_a_fallar=comando.evento_a_fallar
        )
        comando_pulsar = ComandoEjecutarModelos(data=payload)
        self._publicar_mensaje(comando_pulsar, topico, ComandoEjecutarModelos)


    def publicar_comando_compensacion(self, evento, topico):
        payload = ComandoRevertirEjecucionModelosPayload(
            id_dataframe=evento.id_dataframe,
            es_compensacion=True
        )
        evento_gordo=ComandoRevertirEjecucionModelos(data=payload)
        self._publicar_mensaje(evento_gordo, topico, ComandoRevertirEjecucionModelos)