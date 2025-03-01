import pulsar
from pulsar.schema import AvroSchema
import logging
from src.modulos.generacion_data_frames.infraestructura.schema.v1.eventos import DataFramesGeneradosPayload, EventoDataFramesGenerados
from src.modulos.generacion_data_frames.infraestructura.schema.v1.comandos import ComandoEjecutarModelosPayload, ComandoEjecutarModelos
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
            logger.info(f"📤 Publicando mensaje en {topico}: {mensaje}")
            publicador = cliente.create_producer(topico, schema=AvroSchema(schema))
            publicador.send(mensaje)
            logger.info(f"✅ Mensaje publicado con éxito en {topico}")
            cliente.close()
        except Exception as e:
            logger.error(f"❌ Error publicando mensaje en {topico}: {e}")

    def publicar_evento(self, evento, topico):
        """
        Publica el evento `Data Frames Generados` en Pulsar.
        """
        payload = DataFramesGeneradosPayload(
            id=str(evento.id),
            cluster_id=str(evento.cluster_id),
            ruta_archivo_parquet=evento.ruta_archivo_parquet,
            fecha_generacion=evento.fecha_generacion.isoformat()
        )
        evento_pulsar = EventoDataFramesGenerados(data=payload)
        self._publicar_mensaje(evento_pulsar, topico, EventoDataFramesGenerados)

    def publicar_comando(self, comando, topico):
        """
        Publica el comando `Ejecutar Modelos` en Pulsar.
        """
        payload = ComandoEjecutarModelosPayload(
            cluster_id=str(comando.cluster_id),
            ruta_imagen_anonimizada=comando.ruta_imagen_anonimizada
        )
        comando_pulsar = ComandoEjecutarModelos(data=payload)
        self._publicar_mensaje(comando_pulsar, topico, ComandoEjecutarModelos)

    def cerrar(self):
        """
        Cierra la conexión con Pulsar.
        """
        self.cliente.close()
        logger.info("🔌 Cliente Pulsar cerrado.")
