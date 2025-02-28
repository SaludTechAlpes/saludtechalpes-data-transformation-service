import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from src.config.config import Config

# Cargar configuración
config = Config()

# Configuración de la Base de Datos según el entorno
if config.ENVIRONMENT == "test":
    DATABASE_URL = "sqlite:///:memory:"  # Base de datos en memoria para tests
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    DATABASE_URL = f"postgresql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
    engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)

# Configuración de la sesión
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# Definir Base para los modelos ORM
Base = declarative_base()

def get_db():
    """
    Proveedor de sesiones de base de datos.
    Maneja automáticamente la apertura y cierre de sesiones.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
