# SaludTech Alpes - Data Transformation Service

Este repositorio contiene el servicio de transformación de datos para el proyecto **SaludTech Alpes**. Este servicio implementa una arquitectura basada en **eventos y comandos**, utilizando **CQRS** y separación de responsabilidades para garantizar modularidad y escalabilidad.

![Github](https://github.com/SaludTechAlpes/saludtechalpes-data-transformation-service/actions/workflows/action.yaml/badge.svg)
![Github](https://github.com/SaludTechAlpes/saludtechalpes-data-transformation-service/actions/workflows/merge-to-develop.yaml/badge.svg)
![Github](https://github.com/SaludTechAlpes/saludtechalpes-data-transformation-service/actions/workflows/release-to-main.yaml/badge.svg)


## 📂 Estructura del Proyecto

El proyecto sigue una estructura modular organizada por capas de **Dominio, Aplicación e Infraestructura**, siguiendo los principios de **Domain-Driven Design (DDD)**. A continuación, se describe cada parte:

### **1.** **`src/config`**

Contiene la configuración del proyecto:

- `config.py`: Configuraciones generales de la aplicación.
- `db.py`: Configuración de la base de datos y conexión.

### **2.** **`src/modulos`**

Aquí se encuentran los módulos principales del sistema.

#### **2.1 `anonimizacion`**

Este módulo se encarga de anonimizar las imágenes médicas y sus metadatos asociados.

- **`aplicacion`**: Contiene la lógica de aplicación y los servicios encargados de coordinar procesos de negocio.
- **`dominio`**: Define las entidades, reglas de negocio, eventos de dominio y puertos.
- **`infraestructura`**: Implementaciones concretas de los puertos, repositorios, adaptadores y consumidores de eventos.
- **`eventos.py`**: Define los eventos de dominio relacionados con la anonimización de datos.
- **`comandos.py`**: Define los comandos ejecutados dentro del proceso de anonimización.

#### **2.2 `mapeo`**

Este módulo se encarga de agrupar las imágenes anonimizadas en clústers dependiendo de sus metadatos.

- **`aplicacion`**: Contiene la lógica de aplicación y los servicios encargados de coordinar procesos de negocio.
- **`dominio`**: Define las entidades, reglas de negocio, eventos de dominio y puertos.
- **`infraestructura`**: Implementaciones concretas de los puertos, repositorios, adaptadores y consumidores de eventos.
- **`eventos.py`**: Define los eventos de dominio relacionados con la anonimización de datos.
- **`comandos.py`**: Define los comandos ejecutados dentro del proceso de anonimización.

#### **2.3 `ingesta` (Módulo Auxiliar)**

Este módulo maneja la ingesta de datos antes de ser anonimizados. Según la arquitectura diseñada debería estar en un **microservicio separado**, pero para poder evidenciar el correcto funcionamiento de los otros módulos, se ha puesto temporalmente aqui. Sus principales componentes son:

- **`dominio`**: Define los eventos de ingesta.
- **`infraestructura`**: Implementaciones concretas de los puertos expuestos por la capa de dominio.

### **3. `src/seedwork`**

Este módulo contiene código reutilizable para todas las aplicaciones dentro del sistema.

- **`aplicacion`**: Define servicios genéricos, comandos y handlers.
- **`dominio`**: Contiene las abstracciones de entidades, eventos, objetos de valor, reglas de negocio y repositorios.
- **`infraestructura`**: Define implementaciones genéricas de consumidores de eventos, repositorios y en general puertos.

## 🔄 **Flujo de Trabajo del Sistema**

El sistema sigue un flujo basado en **eventos y comandos**:

**Transformacion de datos**: El módulo de procesamiento emite el evento **`Datos agrupados`** y el microservicio emite el evento **`Dataframes generados`**

## 🚀 **Cómo Ejecutar la Aplicación**

### **1. Configuración previa (si no se usa Gitpod)**

Si no estás utilizando Gitpod, es necesario ejecutar los siguientes comandos antes de iniciar la aplicación para el correcto funcionamiento de Pulsar:

```bash
mkdir -p data/bookkeeper && mkdir -p data/zookeeper && sudo chmod -R 777 ./data
```

### **2. Desplegar con Docker Compose**

```bash
make docker-local-up
```
O si no tiene instalado make

```bash
docker compose -f=docker-compose.local.yaml up --build
```

### **3. En caso de errores con Bookkeeper o Zookeeper**

Si los contenedores de **Bookkeeper** o **Zookeeper** fallan o se reinician constantemente, sigue estos pasos:

```bash
make docker-local-down
rm -rf data
mkdir -p data/bookkeeper && mkdir -p data/zookeeper && sudo chmod -R 777 ./data
make docker-up
```

O si no tiene instalado make

```bash
docker compose -f=docker-compose.local.yaml down
rm -rf data
mkdir -p data/bookkeeper && mkdir -p data/zookeeper && sudo chmod -R 777 ./data
make docker-up
```

## 🛠 **Endpoints de la API**

### **1. Verificar estado del servicio**

**Endpoint:** `GET /health`

**Descripción:** Retorna el estado de la aplicación.

**Ejemplo de solicitud con curl:**

```bash
curl -X GET http://localhost:5000/health
```

**Respuesta:**

```json
{
  "status": "up",
  "application_name": "SaludTech Alpes",
  "environment": "development"
}
```

### **2. Simular ingesta de datos**

**Endpoint:** `GET /simular-datos-agrupados`

**Descripción:** Envía un evento de procesamiento de datos ficticio a Pulsar, lo que comienza todo el proceso de transformación de datos.

**Ejemplo de solicitud con curl:**

```bash
curl -X GET http://localhost:5000//simular-datos-agrupados
```

**Respuesta:**

```json
{
  "message": "Evento enviado a Pulsar"
}
```

---
