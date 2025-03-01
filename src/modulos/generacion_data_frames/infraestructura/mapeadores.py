from src.modulos.generacion_data_frames.dominio.entidades import DataFrame
from src.modulos.generacion_data_frames.infraestructura.dto import DataFrameDTO
from src.seedwork.dominio.repositorios import Mapeador

class MapeadorDataFrame(Mapeador):
    """
    Mapeador para convertir entre la entidad `DataFrame` y su DTO `DataFrameDTO`.
    """
    def obtener_tipo(self) -> type:
        return DataFrame

    def entidad_a_dto(self, entidad: DataFrame) -> DataFrameDTO:
        return DataFrameDTO(
            id=entidad.id,
            cluster_id=entidad.cluster_id,
            ruta_archivo_parquet=entidad.ruta_archivo_parquet,
            fecha_generacion=entidad.fecha_generacion
        )

    def dto_a_entidad(self, dto: DataFrameDTO) -> DataFrame:
        return DataFrame(
            id=dto.id,
            cluster_id=dto.cluster_id,
            ruta_archivo_parquet=dto.ruta_archivo_parquet,
            fecha_generacion=dto.fecha_generacion
        )
