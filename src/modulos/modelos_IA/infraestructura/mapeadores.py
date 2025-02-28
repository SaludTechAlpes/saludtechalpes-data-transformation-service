from src.modulos.modelos_IA.dominio.entidades import ModeloIA
from src.modulos.modelos_IA.infraestructura.dto import ModeloIADTO
from src.seedwork.dominio.repositorios import Mapeador


class MapeadorModeloIA(Mapeador):
    def obtener_tipo(self) -> type:
        return ModeloIA.__class__
    
    def entidad_a_dto(self, modelo: ModeloIA) -> ModeloIADTO:
        return ModeloIADTO(
            id=modelo.id,
            nombre=modelo.nombre,
            version=modelo.version,                            
            fecha_entrenamiento=modelo.fecha_entrenamiento,
            endpoint_url=modelo.endpoint_url,
            cluster_id=modelo.cluster_id,
        )

    def dto_a_entidad(self, dto: ModeloIADTO) -> ModeloIA:
        return ModeloIA(
            id=dto.id,
            nombre=dto.nombre,
            version=dto.version,                            
            fecha_entrenamiento=dto.fecha_entrenamiento,
            endpoint_url=dto.endpoint_url,
            cluster_id=dto.cluster_id,
        )
