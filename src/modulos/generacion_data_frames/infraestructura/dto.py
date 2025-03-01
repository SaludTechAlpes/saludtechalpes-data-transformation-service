from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from src.config.db import Base
import uuid
from datetime import datetime, timezone
import os

def get_uuid():
    return str(uuid.uuid4())

class DataFrameDTO(Base):
    """
    Representación de la tabla `data_frames` en PostgreSQL.
    """
    __tablename__ = "data_frames"

    if os.getenv("FLASK_ENV") == "test":
        id = Column(String, primary_key=True, default=get_uuid)
    else:
        id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cluster_id = Column(String, nullable=False)
    ruta_archivo_parquet = Column(String, nullable=False)
    fecha_generacion = Column(DateTime, default=lambda: datetime.now(timezone.utc))
