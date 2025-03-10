from __future__ import annotations
from dataclasses import dataclass, field
import uuid
from datetime import datetime, timezone
from typing import List

from src.seedwork.dominio.entidades import Entidad

@dataclass
class DataFrame(Entidad):
    id: uuid.UUID = None
    ruta_archivo_parquet: str = ""
    fecha_generacion: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    cluster_id: uuid.UUID = None
