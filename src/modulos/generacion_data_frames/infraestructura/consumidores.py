from src.modulos.generacion_data_frames.dominio.comandos import EjecutarModelosComando
from src.seedwork.infraestructura.consumidor_pulsar import ConsumidorPulsar
from src.modulos.generacion_data_frames.infraestructura.schema.v1.eventos import EventoDatosAgrupados
from src.modulos.generacion_data_frames.infraestructura.schema.v1.comandos import ComandoEjecutarModelos
from src.modulos.generacion_data_frames.infraestructura.despachadores import Despachador
from src.modulos.generacion_data_frames.dominio.puertos.procesar_comando_modelos import PuertoProcesarComandoModelos
import pulsar
import logging
from src.config.config import Config


config = Config()

# Configuración de logs
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ConsumidorComandoEjecutarModelos(ConsumidorPulsar):
    """
    Consumidor de comandos de ejecución de modelos en Modelos IA.
    """
    def __init__(self, puerto_modelos: PuertoProcesarComandoModelos):
        cliente = pulsar.Client(f'pulsar://{config.BROKER_HOST}:{config.BROKER_PORT}')
        super().__init__(cliente, "ejecutar-modelos", "saludtech-sub-comandos", ComandoEjecutarModelos)
        self.puerto_modelos = puerto_modelos

    def procesar_mensaje(self, data):
        self.puerto_modelos.procesar_comando_ejecutar_modelos(
            cluster_id=data.cluster_id,
            ruta_imagen_anonimizada=data.ruta_imagen_anonimizada
        )


class ConsumidorEventoDatosAgrupados(ConsumidorPulsar):
    """
    Consumidor de eventos de datos agrupados en Modelos IA.
    """
    despachador = Despachador()

    def __init__(self):
        cliente = pulsar.Client(f'pulsar://{config.EXTERNAL_BROKER_HOST}:{config.EXTERNAL_BROKER_PORT}')
        super().__init__(cliente, "datos-agrupados", "saludtech-sub-eventos", EventoDatosAgrupados)

    def procesar_mensaje(self, data):
        comando_ejecutar = EjecutarModelosComando(
            cluster_id=data.cluster_id,
            ruta_imagen_anonimizada=data.ruta_imagen_anonimizada
        )
        logger.info(f'data: {data}')
        self.despachador.publicar_comando(comando_ejecutar, "ejecutar-modelos")
