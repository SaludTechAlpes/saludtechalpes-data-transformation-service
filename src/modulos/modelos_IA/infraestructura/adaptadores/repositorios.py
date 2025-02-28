from uuid import UUID
from src.modulos.anonimizacion.dominio.puertos.repositorios import RepositorioImagenAnonimizada
from src.modulos.anonimizacion.dominio.entidades import ImagenAnonimizada
from src.modulos.anonimizacion.infraestructura.dto import ImagenAnonimizadaDTO
from src.modulos.anonimizacion.infraestructura.mapeadores import MapeadorImagenAnonimizada
from src.config.db import get_db

class RepositorioModeloIAPostgres(RepositorioImagenAnonimizada):
    def __init__(self):
        self.session = next(get_db())
        self.mapeador = MapeadorImagenAnonimizada()

    def obtener_por_id(self, id: UUID) -> ImagenAnonimizada:
        imagen_dto = self.session.query(ImagenAnonimizadaDTO).filter_by(id=str(id)).one_or_none()
        if not imagen_dto:
            return None
        return self.mapeador.dto_a_entidad(imagen_dto)


    def obtener_todos(self) -> list[ImagenAnonimizada]:
        imagenes_dto = self.session.query(ImagenAnonimizadaDTO).all()
        return [self.mapeador.dto_a_entidad(imagen_dto) for imagen_dto in imagenes_dto]

    def agregar(self, imagen: ImagenAnonimizada):
        imagen_dto = self.mapeador.entidad_a_dto(imagen)

        if imagen_dto.metadatos:
            self.session.add(imagen_dto.metadatos)

        self.session.add(imagen_dto)
        self.session.commit()

    def actualizar(self, imagen: ImagenAnonimizada):
        imagen_dto = self.mapeador.entidad_a_dto(imagen)
        self.session.merge(imagen_dto)
        self.session.commit()

    def eliminar(self, id: UUID):
        self.session.query(ImagenAnonimizadaDTO).filter_by(id=str(id)).delete()
        self.session.commit()
