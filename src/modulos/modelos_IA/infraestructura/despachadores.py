import pulsar
from pulsar.schema import AvroSchema
import json
import logging
from src.modulos.modelos_IA.infraestructura.schema.v1.eventos import PipelinesModelosEjecutadosPayload, EventoPipelinesModelosEjecutados
from src.modulos.modelos_IA.infraestructura.schema.v1.comandos import ComandoEjecutarPipelinesModelosPayload, ComandoEjecutarPipelinesModelos
from src.config.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
config = Config()

class DespachadorModelosIA:
    def _publicar_mensaje(self, mensaje, topico, schema):
        try:
            cliente = pulsar.Client(f'{config.PULSAR_HOST}://{config.BROKER_HOST}:6650')
            logger.info(f"Publicando mensaje en {topico}: {mensaje}")
            publicador = cliente.create_producer(topico, schema=AvroSchema(schema))
            publicador.send(mensaje)
            logger.info(f"Mensaje publicado con éxito en {topico}")
            cliente.close()
        except Exception as e:
            logger.error(f"Error publicando mensaje en {topico}: {e}")

    def publicar_evento(self, evento, topico):
        payload = PipelinesModelosEjecutadosPayload(
            cluster_id=str(evento.cluster_id),
            ruta_imagen_anonimizada=evento.ruta_imagen_anonimizada,
            resultados_modelos=evento.resultados_modelos,
        )
        evento_gordo = EventoPipelinesModelosEjecutados(data=payload)
        self._publicar_mensaje(evento_gordo, topico, EventoPipelinesModelosEjecutados)

    def publicar_comando(self, comando, topico):
        payload = ComandoEjecutarPipelinesModelosPayload(
            cluster_id=str(comando.cluster_id),
            ruta_imagen_anonimizada=comando.ruta_imagen_anonimizada
        )
        comando_gordo = ComandoEjecutarPipelinesModelos(data=payload)
        self._publicar_mensaje(comando_gordo, topico, ComandoEjecutarPipelinesModelos)

    def cerrar(self):
        self.cliente.close()
        logger.info("Cliente Pulsar cerrado.")
