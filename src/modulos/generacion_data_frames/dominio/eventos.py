from __future__ import annotations
from dataclasses import dataclass
import uuid
from datetime import datetime
from typing import Optional
from src.seedwork.dominio.eventos import EventoDominio

@dataclass
class DataFramesGeneradosEvento(EventoDominio):
    """
    Evento de Dominio que indica que un DataFrame ha sido generado y almacenado.
    """
    id_dataframe: Optional[str] = None
    cluster_id: Optional[str] = None
    ruta_archivo_parquet: Optional[str] = None
    fecha_generacion: Optional[datetime] = None
    evento_a_fallar: Optional[str] = None


@dataclass
class DatosAgrupadosEvento(EventoDominio):
    """
    Evento de Dominio que indica que los datos han sido agrupados y están listos para procesarse.
    """
    id_imagen_importada: Optional[uuid.UUID] = None
    id_imagen_anonimizada: Optional[uuid.UUID] = None
    id_imagen_mapeada: Optional[uuid.UUID] = None
    cluster_id: Optional[uuid.UUID] = None
    ruta_imagen_anonimizada: Optional[str] = None
    evento_a_fallar: Optional[str] = None

@dataclass
class DataFramesGeneradosFallidoEvento(EventoDominio):
    id_imagen_importada: Optional[uuid.UUID] = None
    id_imagen_anonimizada: Optional[uuid.UUID] = None
    id_imagen_mapeada: Optional[uuid.UUID] = None
    id_dataframe: Optional[str] = None
