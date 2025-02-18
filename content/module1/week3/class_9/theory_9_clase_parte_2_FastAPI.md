# Introducción a Pydantic

## ¿Qué es Pydantic?:

- Biblioteca para validar datos usando tipos de Python y anotaciones.

- Ideal para definir esquemas de entrada/salida en APIs.

## Modelos de Datos:

Ejemplo de modelo con validación:

```python
from pydantic import BaseModel, Field  

class Producto(BaseModel):  
    nombre: str  
    precio: float = Field(gt=0, description="El precio debe ser positivo")  
    stock: int = Field(ge=0, description="El stock no puede ser negativo")  
```

## Integración con FastAPI:

Los modelos de Pydantic se usan directamente en los parámetros de las rutas.

Ejemplo:
```python
@app.post("/productos/")  
def crear_producto(producto: Producto):  
    return producto  
```