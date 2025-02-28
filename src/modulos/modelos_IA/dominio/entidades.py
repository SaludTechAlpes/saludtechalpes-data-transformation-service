from __future__ import annotations
from dataclasses import dataclass, field
import uuid
from datetime import datetime, timezone
from typing import List

import src.modulos.modelos_IA.dominio.objetos_valor as ov
from src.seedwork.dominio.entidades import Entidad

@dataclass
class ModeloIA:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    nombre: str = ""
    version: str = ""                                 
    fecha_entrenamiento: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    endpoint_url: str = ""
    cluster_id: uuid.UUID = field(default_factory=uuid.uuid4)
