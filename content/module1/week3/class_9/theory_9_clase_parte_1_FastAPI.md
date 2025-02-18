# Introducción a FastAPI

## Definición:
Framework de alto rendimiento para construir APIs con Python 3.7+, basado en estándares como OpenAPI y JSON Schema.

## Características principales:

- Soporta ASGI (Asynchronous Server Gateway Interface) para manejar conexiones asíncronas.
- Genera documentación automática interactiva (Swagger UI y Redoc).
- Integración nativa con Pydantic para validación de datos.

## Comparación con otros frameworks:

- Flask: Ideal para aplicaciones pequeñas, pero sin validación automática o soporte asíncrono integrado.
- Django: Potente para aplicaciones web completas, pero más complejo y menos optimizado para APIs modernas.

## Ventajas de FastAPI

### Rendimiento:

Comparable a Node.js y Go gracias a ASGI y Uvicorn (servidor web asíncrono).

Ejemplo: Maneja miles de solicitudes por segundo con bajo consumo de recursos.

### Validación Automática:

Usa Pydantic para definir modelos de datos y validar entradas/salidas.

Ejemplo de modelo:

```python
from pydantic import BaseModel  

class Usuario(BaseModel):  
    nombre: str  
    edad: int  
```
### Documentación Autogenerada:

Accesible en /docs y /redoc.


## Conceptos Clave de FastAPI 

### Rutas (Endpoints):
- Definidas con decoradores: @app.get(), @app.post(), etc.
- Ejemplo básico:

```python
@app.get("/items/{item_id}")  
def leer_item(item_id: int):  
    return {"item_id": item_id}   
```
### Tipos de Parámetros:

- Path parameters: Variables en la URL (/{item_id}).
- Query parameters: Filtros opcionales (?skip=0&limit=10).
- Body parameters: Datos enviados en el cuerpo de la solicitud (para POST/PUT).

# Respuestas HTTP:

- Códigos de estado personalizados (ej: status.HTTP_201_CREATED).
- Manejo de errores con HTTPException.
