from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from src.config.db import Base
import uuid
import os
from datetime import datetime, timezone

def get_uuid():
    return str(uuid.uuid4())

def default_list():
    return []

class ModeloIADTO(Base):    
    __tablename__ = "modelos_ia"

    if os.getenv("FLASK_ENV") == "test":
        id = Column(String, primary_key=True, default=get_uuid)
        cluster_id = Column(String, nullable=False)
    else:
        id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        cluster_id = Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4)

    nombre = Column(String, nullable=False)
    version = Column(String, nullable=False)
    fecha_entrenamiento = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    endpoint_url = Column(String, nullable=False)