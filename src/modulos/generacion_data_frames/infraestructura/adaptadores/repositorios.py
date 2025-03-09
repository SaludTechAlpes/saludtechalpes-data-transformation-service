from uuid import UUID
from sqlalchemy import delete
from src.modulos.generacion_data_frames.dominio.puertos.repositorios import RepositorioDataFrame
from src.modulos.generacion_data_frames.dominio.entidades import DataFrame
from src.modulos.generacion_data_frames.infraestructura.dto import DataFrameDTO
from src.modulos.generacion_data_frames.infraestructura.mapeadores import MapeadorDataFrame
from src.config.db import get_db

class RepositorioDataFramePostgres(RepositorioDataFrame):
    def __init__(self):
        self.session = next(get_db())
        self.mapeador = MapeadorDataFrame()

    def obtener_por_id(self, id: UUID) -> DataFrame:
        dataframe_dto = self.session.query(DataFrameDTO).filter_by(id=str(id)).one_or_none()
        if not dataframe_dto:
            return None
        return self.mapeador.dto_a_entidad(dataframe_dto)

    def obtener_todos(self) -> list[DataFrame]:
        dataframes_dto = self.session.query(DataFrameDTO).all()
        return [self.mapeador.dto_a_entidad(dataframe_dto) for dataframe_dto in dataframes_dto]

    def agregar(self, dataframe: DataFrame):
        dataframe_dto = self.mapeador.entidad_a_dto(dataframe)
        self.session.add(dataframe_dto)
        self.session.commit()

    def actualizar(self, dataframe: DataFrame):
        dataframe_dto = self.mapeador.entidad_a_dto(dataframe)
        self.session.merge(dataframe_dto)
        self.session.commit()

    def eliminar(self, id: UUID):
        self.session.execute(
            delete(DataFrameDTO).where(DataFrameDTO.id == str(id))
        )
        self.session.commit()
