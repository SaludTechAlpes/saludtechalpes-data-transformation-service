import os
import pulsar
import logging
import threading

from flask import Flask, jsonify, request
from src.config.config import Config
from src.config.db import Base, engine

# Importación de módulos de Generación de DataFrames
from src.modulos.generacion_data_frames.aplicacion.servicios import ServicioAplicacionGeneracionDataFrames
from src.modulos.generacion_data_frames.infraestructura.adaptadores.ejecutar_modelos import AdaptadorEjecutarModelosIA
from src.modulos.generacion_data_frames.infraestructura.adaptadores.repositorios import RepositorioDataFramePostgres
from src.modulos.generacion_data_frames.infraestructura.consumidores import (
    ConsumidorComandoEjecutarModelos,
    ConsumidorEventoDatosAgrupados,
    ConsumidorComandoRevertirEjecucionModelos
)
from src.modulos.generacion_data_frames.infraestructura.despachador_datos_agrupados import DespachadorDatosAgrupados
from src.modulos.generacion_data_frames.infraestructura.despachadores import Despachador
from src.modulos.generacion_data_frames.dominio.eventos import DatosAgrupadosEvento
from src.modulos.generacion_data_frames.dominio.comandos import RevertirEjecucionModelosComando

# Configuración de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración de Pulsar
config = Config()

def comenzar_consumidor():
    """
    Inicia los consumidores en hilos separados.
    """

    if os.getenv("FLASK_ENV") == "test":
        logger.info("🔹 Saltando inicio de consumidores en modo test")
        return

    # Crear dependencias del servicio de aplicación
    adaptador_modelos = AdaptadorEjecutarModelosIA()
    repositorio_dataframes = RepositorioDataFramePostgres()

    # Instanciar el servicio de aplicación
    servicio_generacion_dataframes = ServicioAplicacionGeneracionDataFrames(adaptador_modelos, repositorio_dataframes)

    # Iniciar consumidores en hilos separados
    consumidor_eventos_datos_agrupados = ConsumidorEventoDatosAgrupados()
    threading.Thread(target=consumidor_eventos_datos_agrupados.suscribirse, daemon=True).start()
    
    consumidor_comandos_ejecutar_modelos = ConsumidorComandoEjecutarModelos(servicio_generacion_dataframes)
    threading.Thread(target=consumidor_comandos_ejecutar_modelos.suscribirse, daemon=True).start()

    consumidor_comandos_revertir_ejecucion = ConsumidorComandoRevertirEjecucionModelos(servicio_generacion_dataframes)
    threading.Thread(target=consumidor_comandos_revertir_ejecucion.suscribirse, daemon=True).start()

def create_app(configuracion=None):
    app = Flask(__name__, instance_relative_config=True)

    with app.app_context():
        if app.config.get('TESTING'):
            app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        Base.metadata.create_all(engine)
        if not app.config.get('TESTING'):
            comenzar_consumidor()

    despachador_generacion_dataframes = DespachadorDatosAgrupados()
    despachador = Despachador()

    @app.route("/health")
    def health():
        return {
            "status": "up",
            "application_name": config.APP_NAME,
            "environment": config.ENVIRONMENT
        }

    @app.route("/simular-datos-agrupados", methods=["POST"])
    def simular_datos_agrupados():
        """
        Endpoint para probar la publicación del evento `Datos Agrupados` en Pulsar.
        """
        try:
            data = request.get_json()
            id_imagen_importada = data.get("id_imagen_importada", None)
            id_imagen_anonimizada = data.get("id_imagen_anonimizada", None)
            id_imagen_mapeada = data.get("id_imagen_mapeada", None)
            evento_a_fallar = data.get("evento_a_fallar", None)

            evento_prueba = DatosAgrupadosEvento(
                id_imagen_importada = id_imagen_importada,
                id_imagen_anonimizada = id_imagen_anonimizada,
                id_imagen_mapeada = id_imagen_mapeada,
                cluster_id = "id_cluster_patologia",
                ruta_imagen_anonimizada = "ruta_imagen_anonimizada",
                evento_a_fallar=evento_a_fallar
            )

            if not app.config.get('TESTING'):
                despachador_generacion_dataframes.publicar_evento(evento_prueba, "datos-agrupados")

            return jsonify({"message": "Evento publicado en `datos-agrupados`"}), 200
        except Exception as e:
            logger.error(f"❌ Error al publicar evento en `datos-agrupados`: {e}")
            return jsonify({"error": "Error al publicar evento en `datos-agrupados`"}), 500


    @app.route("/simular-dataframes-comando-compensacion", methods=["POST"])
    def simular_dataframes_comando_compensacion():
        try:
            data = request.get_json()
            id_dataframe = data.get("id_dataframe", None)
            
            comando = RevertirEjecucionModelosComando(
                id_dataframe=id_dataframe
            )

            if not app.config.get('TESTING'):
                despachador.publicar_comando_compensacion(comando, "revertir-ejecucion-modelos")

            return jsonify({"message": "Evento de compensacion publicado en `revertir-ejecucion-modelos`"}), 200
        
        except Exception as e:
            logger.error(f"❌ Error al publicar evento de compensación en `revertir-ejecucion-modelos`: {e}")
            return jsonify({"error": "Error al publicar evento de compensacion en `revertir-ejecucion-modelos`"}), 500

    return app
