from pulsar.schema import *
from src.seedwork.infraestructura.schema.v1.comandos import ComandoIntegracion

class ComandoEjecutarModelosPayload(Record):
    """
    Payload del comando `Ejecutar Modelos`.
    Contiene los datos necesarios para iniciar la ejecución de modelos IA.
    """
    cluster_id = String()
    ruta_imagen_anonimizada = String()

class ComandoEjecutarModelos(ComandoIntegracion):
    """
    Comando de integración que indica que se deben ejecutar modelos IA.
    """
    data = ComandoEjecutarModelosPayload()