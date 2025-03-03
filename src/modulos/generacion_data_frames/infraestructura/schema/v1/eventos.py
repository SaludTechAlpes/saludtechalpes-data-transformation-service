from pulsar.schema import *
from src.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class DataFramesGeneradosPayload(Record):
    cluster_id = String()
    ruta_archivo_parquet = String()
    fecha_generacion = String()
    

class EventoDataFramesGenerados(EventoIntegracion):
    data = DataFramesGeneradosPayload()


class DatosAgrupadosPayload(Record):
    cluster_id = String()
    ruta_imagen_anonimizada = String()
  
class EventoDatosAgrupados(EventoIntegracion):
    data = DatosAgrupadosPayload()