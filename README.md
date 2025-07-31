# API de Procesamiento de Mensajes de Chat

## Descripción
API RESTful desarrollada con FastAPI para el procesamiento y almacenamiento de mensajes de chat. La aplicación implementa un sistema completo de validación, procesamiento y recuperación de mensajes.

## Características
- ✅ Endpoint POST para crear mensajes
- ✅ Endpoint GET para recuperar mensajes por sesión
- ✅ Validación de formato de mensajes
- ✅ Filtrado de contenido inapropiado
- ✅ Almacenamiento en base de datos SQLite
- ✅ Paginación y filtrado
- ✅ Manejo de errores robusto
- ✅ Pruebas unitarias completas
- ✅ Documentación automática con Swagger

## Instalación

1. Clonar el repositorio
2. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Ejecución

### 🐳 Con Docker (Recomendado)

La forma más fácil de ejecutar la aplicación es usando Docker:

```bash
chmod +x docker-run.sh

./docker-run.sh run

./docker-run.sh dev

./docker-run.sh logs

./docker-run.sh stop
```

Para más información sobre Docker, consulta [DOCKER.md](DOCKER.md).

### 🔧 Sin Docker

#### Desarrollo
```bash
uvicorn app.main:app --reload
```

#### Producción
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Documentación de la API

Una vez ejecutada la aplicación, puedes acceder a:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Estructura del Proyecto

```
app/
├── __init__.py
├── main.py                 # Punto de entrada de la aplicación
├── config.py              # Configuración de la aplicación
├── models/
│   ├── __init__.py
│   ├── message.py         # Modelos de datos
│   └── database.py        # Configuración de base de datos
├── schemas/
│   ├── __init__.py
│   └── message.py         # Esquemas Pydantic
├── repositories/
│   ├── __init__.py
│   └── message_repository.py  # Capa de acceso a datos
├── services/
│   ├── __init__.py
│   └── message_service.py     # Lógica de negocio
├── controllers/
│   ├── __init__.py
│   └── message_controller.py  # Controladores de API
└── utils/
    ├── __init__.py
    ├── content_filter.py      # Filtrado de contenido
    └── exceptions.py          # Excepciones personalizadas

tests/
├── __init__.py
├── conftest.py            # Configuración de pruebas
├── test_message_controller.py
├── test_message_service.py
└── test_message_repository.py
```

## Endpoints

### POST /api/messages
Crea un nuevo mensaje.

**Body:**
```json
{
  "message_id": "msg_123",
  "session_id": "session_456",
  "content": "Hola mundo",
  "timestamp": "2023-12-01T10:00:00Z",
  "sender": "user"
}
```

### GET /api/messages/{session_id}
Recupera mensajes por sesión con paginación y filtros.

**Parámetros:**
- `session_id`: ID de la sesión
- `limit`: Número máximo de mensajes (default: 10)
- `offset`: Número de mensajes a saltar (default: 0)
- `sender`: Filtrar por remitente ("user" o "system")

## Pruebas

Ejecutar todas las pruebas:
```bash
pytest
```

Ejecutar con cobertura:
```bash
pytest --cov=app
```

## Tecnologías Utilizadas

- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: ORM para base de datos
- **Pydantic**: Validación de datos
- **SQLite**: Base de datos ligera
- **Pytest**: Framework de pruebas
- **Uvicorn**: Servidor ASGI
- **Docker**: Contenerización de la aplicación

## Arquitectura

El proyecto sigue los principios de **Arquitectura Limpia**:

- **Controllers**: Manejan las peticiones HTTP
- **Services**: Contienen la lógica de negocio
- **Repositories**: Gestionan el acceso a datos
- **Models**: Definen las entidades de datos
- **Schemas**: Validan los datos de entrada/salida

## Manejo de Errores

La API incluye manejo robusto de errores con códigos HTTP apropiados:
- `400 Bad Request`: Datos de entrada inválidos
- `404 Not Found`: Recurso no encontrado
- `422 Unprocessable Entity`: Validación fallida
- `500 Internal Server Error`: Errores del servidor 