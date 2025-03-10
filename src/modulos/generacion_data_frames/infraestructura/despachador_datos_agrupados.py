import pulsar
from pulsar.schema import AvroSchema
import logging
from src.modulos.generacion_data_frames.infraestructura.schema.v1.eventos import DatosAgrupadosPayload, EventoDatosAgrupados
from src.config.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
config = Config()

class DespachadorDatosAgrupados:
    """
    Despachador para publicar el evento `Datos Agrupados` en Apache Pulsar.
    """

    def _publicar_mensaje(self, mensaje, topico, schema):
        """
        Método interno para publicar un mensaje en Pulsar.
        """
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
        """
        Publica el evento `Datos Agrupados` en Pulsar.
        """
        payload = DatosAgrupadosPayload(
            id_imagen_importada = str(evento.id_imagen_importada),
            id_imagen_anonimizada = str(evento.id_imagen_anonimizada),
            id_imagen_mapeada = str(evento.id_imagen_mapeada),
            cluster_id=str(evento.cluster_id),
            ruta_imagen_anonimizada=evento.ruta_imagen_anonimizada,
            evento_a_fallar = evento.evento_a_fallar
        )
        evento_pulsar = EventoDatosAgrupados(data=payload)
        self._publicar_mensaje(evento_pulsar, topico, EventoDatosAgrupados)
