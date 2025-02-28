from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from src.config.db import Base
import uuid
from datetime import datetime, timezone

class DataFrameDTO(Base):
    """
    Representación de la tabla `data_frames` en PostgreSQL.
    """
    __tablename__ = "data_frames"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cluster_id = Column(String, nullable=False)  # Identificador del Cluster
    ruta_archivo_parquet = Column(String, nullable=False)  # Ruta en la nube
    fecha_generacion = Column(DateTime, default=lambda: datetime.now(timezone.utc))
