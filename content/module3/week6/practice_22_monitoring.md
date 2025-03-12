# Clase 22: Introducción teórica al Monitoreo de Aplicaciones
El monitoreo de aplicaciones es el proceso de recopilar, analizar y visualizar datos sobre el comportamiento y rendimiento de una aplicación con el objetivo de detectar problemas, optimizar el uso de recursos y garantizar un funcionamiento eficiente.

## ¿Por qué es importante el monitoreo?
El monitoreo permite:
- Detección temprana de errores: Identificar fallos antes de que impacten a los usuarios.
- Optimización de rendimiento: Reducir tiempos de respuesta y consumo de recursos.
- Seguridad y auditoría: Detectar accesos no autorizados o anomalías.
- Control de costos: En el caso de servicios en la nube o APIs de terceros (como OpenAI), evitar gastos innecesarios.

## Tipos de Monitoreo
Existen diferentes enfoques para el monitoreo de aplicaciones:

### Monitoreo de Rendimiento (APM - Application Performance Monitoring): Evalúa la velocidad y eficiencia de la aplicación, midiendo:
- Tiempo de respuesta de API y servicios
- Uso de CPU y memoria
- Latencia en bases de datos

### Monitoreo de Registros (Logging): Registra eventos importantes para análisis y debugging:
- Errores y excepciones
- Peticiones de usuarios y respuestas del sistema
- Eventos críticos como reinicios o fallos

### Monitoreo de Costos: Para aplicaciones que consumen servicios de terceros (como OpenAI), se mide:
- Cantidad de requests
- Tokens utilizados
- Costo total por API


## Setup Inicial

### Estructura recomendada para organizar los scripts de monitoreo en tu aplicación FastAPI:

```bash
📂 mi_proyecto/
│── 📂 app/
│   │── 📂 monitoring/         # Módulo de monitoreo
│   │   │── performance.py     # Monitoreo de rendimiento (APM)
│   │   │── logging.py         # Monitoreo de errores (Logging)
│   │   │── costs.py           # Monitoreo de costos (OpenAI)
│   │── main.py                # Punto de entrada de FastAPI
│   │── database.py            # Conexión con Supabase
│── .env                       # Variables de entorno (Supabase, OpenAI)
│── requirements.txt           # Dependencias del proyecto
│── README.md                  # Documentación
```

### Configuración:
1. 📂 app/main.py
```python
from fastapi import FastAPI, Request, HTTPException
from app.monitoring.performance import measure_request_time
from app.monitoring.logging import log_error
from app.monitoring.costs import log_openai_cost
from app.database import supabase_client
from openai import OpenAI
import os

app = FastAPI()

# Cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Middleware de monitoreo de rendimiento (APM)
app.middleware("http")(measure_request_time)

@app.get("/")
async def root():
    return {"message": "API de monitoreo en ejecución 🚀"}

# Endpoint para probar errores y monitoreo de logging
@app.get("/error")
async def trigger_error():
    try:
        1 / 0  # Error forzado
    except Exception as e:
        log_error("/error", str(e))
        raise HTTPException(status_code=500, detail="Error interno registrado")

# Endpoint para generar respuesta con OpenAI y monitorear costos
@app.post("/generate")
async def generate_response(prompt: str, model: str = "gpt-3.5-turbo"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )

        tokens_used = response.usage.total_tokens
        cost = log_openai_cost(model, tokens_used)

        return {"response": response.choices[0].message.content, "tokens_used": tokens_used, "cost": cost}
    except Exception as e:
        log_error("/generate", str(e))
        raise HTTPException(status_code=500, detail="Error generando respuesta")
```

2. 📂 app/database.py
```python
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

supabase_client: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)
```

3. Instala dependencias:
```bash
pip install fastapi openai supabase
```

4. Configura .env con tus claves:
```python
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
OPENAI_API_KEY=your_openai_key
```

5. Ejecuta FastAPI:
```bash
uvicorn app.main:app --reload
```

## Ejercicio 1: Monitoreo de Rendimiento (APM)
Mide el tiempo de ejecución de una función en FastAPI y almacena los resultados en Supabase.

1. Crear la tabla performance_logs en Supabase con columnas timestamp, endpoint, method, response_time.

| Columna        | Tipo de dato   | Descripción                                       |
|---------------|---------------|---------------------------------------------------|
| `id`          | `uuid` (PK)    | Identificador único (generado automáticamente)   |
| `timestamp`   | `timestamptz`  | Fecha y hora de la request (UTC)                 |
| `endpoint`    | `text`         | Ruta del endpoint accedido (`/generate`, `/error`, etc.) |
| `method`      | `text`         | Método HTTP (`GET`, `POST`, etc.)                 |
| `response_time` | `float8`     | Tiempo de respuesta en segundos                   |


2. En el archivo app/monitoring/performance.py (Monitoreo de rendimiento)
Define el middleware que mide el tiempo de respuesta de las requests.

```python
import time
from fastapi import Request
import supabase
from datetime import datetime
from app.database import supabase_client  # Importar conexión a Supabase

TABLE_NAME = "performance_logs"

async def measure_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "endpoint": request.url.path,
        "method": request.method,
        "response_time": duration
    }
    supabase_client.table(TABLE_NAME).insert(log_data).execute()

    return response
```

3. Hacer requests a la API y verificar los tiempos en Supabase.

**Ejercicio extra:** Agregar un filtro para monitorear solo ciertos endpoints.


---
## Ejercicio 2: Monitoreo de Registros (Logging)
Captura y almacena errores en la API en Supabase.

1. Crear la tabla error_logs en Supabase con columnas timestamp, error_message, endpoint.
| Columna        | Tipo de dato   | Descripción                             |
|---------------|---------------|-----------------------------------------|
| `id`          | `uuid` (PK)    | Identificador único (generado automáticamente) |
| `timestamp`   | `timestamptz`  | Fecha y hora del error                  |
| `endpoint`    | `text`         | Ruta donde ocurrió el error             |
| `error_message` | `text`       | Mensaje del error       

2. En el archivo app/monitoring/logging.py (Monitoreo de errores)
Guarda los errores en Supabase.
```python
import logging
import supabase
from datetime import datetime
from app.database import supabase_client

TABLE_NAME = "error_logs"

logging.basicConfig(level=logging.ERROR)

def log_error(endpoint: str, error_message: str):
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "error_message": error_message,
        "endpoint": endpoint
    }
    supabase_client.table(TABLE_NAME).insert(log_data).execute()
    logging.error(f"Error en {endpoint}: {error_message}")
```

3. Generar errores intencionales y verificar los logs en Supabase.

**Ejercicio extra:** Mejorar el código para capturar más detalles

---
## Ejercicio 3: Monitoreo de Costos
Registrar el costo de cada request a OpenAI en Supabase.

1. Crear la tabla cost_logs en Supabase con columnas timestamp, model, tokens_used, cost.
| Columna       | Tipo de dato   | Descripción                               |
|--------------|---------------|-------------------------------------------|
| `id`         | `uuid` (PK)    | Identificador único (generado automáticamente) |
| `timestamp`  | `timestamptz`  | Fecha y hora del request                  |
| `model`      | `text`         | Modelo de OpenAI usado (`gpt-3.5-turbo`, `gpt-4`, etc.) |
| `tokens_used` | `int4`        | Cantidad de tokens consumidos             |
| `cost`       | `float8`       | Costo en dólares del request   

2. En el archivo app/monitoring/costs.py (Monitoreo de costos)
Registra los costos de OpenAI.
```python
from openai import OpenAI
import supabase
from datetime import datetime
from app.database import supabase_client
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

TABLE_NAME = "cost_logs"

TOKEN_COSTS = {"gpt-4": 0.03 / 1000, "gpt-3.5-turbo": 0.002 / 1000}

def log_openai_cost(model: str, tokens_used: int):
    cost = tokens_used * TOKEN_COSTS.get(model, 0)
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "model": model,
        "tokens_used": tokens_used,
        "cost": cost
    }
    supabase_client.table(TABLE_NAME).insert(log_data).execute()
    return cost
```

3. Probar con diferentes prompts y verificar el costo en Supabase.

**Ejercicio extra:** Implementar una alerta si el costo diario supera un límite.