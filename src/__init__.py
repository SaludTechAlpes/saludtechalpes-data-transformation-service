import os
import pulsar
import logging
import threading

from flask import Flask, jsonify
from src.config.config import Config
from src.config.db import Base, engine

# Importación de módulos de Generación de DataFrames
from src.modulos.generacion_data_frames.aplicacion.servicios import ServicioAplicacionGeneracionDataFrames
from src.modulos.generacion_data_frames.infraestructura.adaptadores.ejecutar_modelos import AdaptadorEjecutarModelosIA
from src.modulos.generacion_data_frames.infraestructura.adaptadores.repositorios import RepositorioDataFramePostgres
from src.modulos.generacion_data_frames.infraestructura.consumidores import (
    ConsumidorComandoEjecutarModelos,
    ConsumidorEventoDatosAgrupados
)
from src.modulos.generacion_data_frames.infraestructura.despachador_datos_agrupados import DespachadorDatosAgrupados
from src.modulos.generacion_data_frames.dominio.eventos import DatosAgrupadosEvento

# Configuración de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración de Pulsar
config = Config()
pulsar_cliente = None
if os.getenv("FLASK_ENV") != "test":
    pulsar_cliente = pulsar.Client(f'pulsar://{config.BROKER_HOST}:6650')

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

def create_app(configuracion=None):
    global pulsar_cliente

    app = Flask(__name__, instance_relative_config=True)

    with app.app_context():
        if app.config.get('TESTING'):
            app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        Base.metadata.create_all(engine)
        if not app.config.get('TESTING'):
            comenzar_consumidor()

    despachador_generacion_dataframes = DespachadorDatosAgrupados()

    @app.route("/health")
    def health():
        return {
            "status": "up",
            "application_name": config.APP_NAME,
            "environment": config.ENVIRONMENT
        }

    @app.route("/simular-datos-agrupados", methods=["GET"])
    def simular_datos_agrupados():
        """
        Endpoint para probar la publicación del evento `Datos Agrupados` en Pulsar.
        """
        try:
            evento_prueba = DatosAgrupadosEvento(
                cluster_id="rayosx_torax_neumonia",
                ruta_imagen_anonimizada="/simulacion/imagenes/imagen_1234.dcm"
            )

            if not app.config.get('TESTING'):
                despachador_generacion_dataframes.publicar_evento(evento_prueba, "datos-agrupados")

            return jsonify({"message": "Evento publicado en `datos-agrupados`"}), 200
        except Exception as e:
            logger.error(f"Error al publicar evento de prueba: {e}")
            return jsonify({"error": "Error al publicar evento en Pulsar"}), 500


    # Cerrar Pulsar cuando la aplicación termina
    @app.teardown_appcontext
    def cerrar_pulsar(exception=None):
        global pulsar_cliente
        if pulsar_cliente:
            pulsar_cliente.close()
            logger.info("Cliente Pulsar cerrado al detener Flask.")

    return app
