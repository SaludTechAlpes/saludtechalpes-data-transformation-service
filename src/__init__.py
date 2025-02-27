import os
import pulsar
import json
import logging
import threading

from flask import Flask, jsonify
from src.config.config import Config
from src.modulos.ingesta.infraestructura.despachadores import Despachador
from src.modulos.ingesta.dominio.eventos import DatosImportadosEvento
from src.modulos.anonimizacion.infraestructura.consumidores_comandos import ConsumidorComandosAnonimizacion
from src.modulos.anonimizacion.infraestructura.consumidores_eventos import ConsumidorEventosIngesta
from src.modulos.anonimizacion.aplicacion.servicios import ServicioAplicacionAnonimizacion
from src.modulos.anonimizacion.infraestructura.adaptadores.anonimizar_datos import AdaptadorAnonimizarDatos
from src.modulos.anonimizacion.infraestructura.adaptadores.repositorios import RepositorioImagenAnonimizadaPostgres
from src.config.db import Base, engine

# Configuración de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Identifica el directorio base
basedir = os.path.abspath(os.path.dirname(__file__))
config = Config()

pulsar_cliente = None
if os.getenv("FLASK_ENV") != "test":
    pulsar_cliente = pulsar.Client(f'{os.getenv("PULSAR_HOST")}://{os.getenv("BROKER_HOST")}:6650')

def comenzar_consumidor():
    """
    Inicia el consumidor en un hilo separado, pasando el servicio de aplicación.
    """

    if os.getenv("FLASK_ENV") == "test":
        logger.info("🔹 Saltando inicio de consumidores en modo test")
        return
    # Crear las dependencias del servicio de aplicación
    adaptador_anonimizacion = AdaptadorAnonimizarDatos()
    repositorio_imagenes = RepositorioImagenAnonimizadaPostgres()
    
    # Instanciar el servicio de aplicación con sus dependencias
    servicio_anonimizacion = ServicioAplicacionAnonimizacion(adaptador_anonimizacion, repositorio_imagenes)

    consumidor_eventos = ConsumidorEventosIngesta()
    threading.Thread(target=consumidor_eventos.suscribirse, daemon=True).start()
    
    consumidor_comandos = ConsumidorComandosAnonimizacion(servicio_anonimizacion)
    threading.Thread(target=consumidor_comandos.suscribirse, daemon=True).start()

def create_app(configuracion=None):
    global pulsar_cliente

    app = Flask(__name__, instance_relative_config=True)

    with app.app_context():
        if app.config.get('TESTING'):
            app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        Base.metadata.create_all(engine) 
        if not app.config.get('TESTING'):
            comenzar_consumidor()

    despachador_ingesta = Despachador()

    

    @app.route("/health")
    def health():
        return {
            "status": "up",
            "application_name": config.APP_NAME,
            "environment": config.ENVIRONMENT
        }


    # Cerrar Pulsar cuando la aplicación termina
    @app.teardown_appcontext
    def cerrar_pulsar(exception=None):
        global pulsar_cliente
        if pulsar_cliente:
            pulsar_cliente.close()
            logger.info("Cliente Pulsar cerrado al detener Flask.")

    return app
