# Introducción a Pydantic

## Descripción
Aplicaremos los conceptos teóricos creando modelos Pydantic para usuarios y productos, integrando validaciones personalizadas y manejando errores en una API real.

## Objetivos
- Crear modelos Pydantic con validaciones personalizadas.
- Integrar modelos en endpoints POST y PUT.
- Probar errores de validación en Swagger UI.

## Actividades

### Ejercicio 1: Modelo de Usuario con Validaciones

Crea un modelo para registrar usuarios con email y contraseña segura.

1. Crea un archivo main.py en PyCharm.

2. Instala las dependencias:

```bash
pip install pydantic email-validator  
```

3. Escribir el código

```python
from fastapi import FastAPI  

app = FastAPI()  

@app.get("/")  
def hola_mundo():  
    return {"mensaje": "¡Bienvenido a FastAPI!"}  
```

4. Ejecutar la API
```bash
uvicorn main:app --reload  
```

5. Definir el modelo

```python
from pydantic import BaseModel, EmailStr, Field  

class UsuarioRegistro(BaseModel):  
    nombre: str = Field(min_length=3, example="Ana")  
    email: EmailStr = Field(example="ana@example.com")  
    password: str = Field(min_length=8, example="password123")  
```

6. Endpoint POST

```python
@app.post("/registro/")  
def registrar_usuario(usuario: UsuarioRegistro):  
    return {  
        "mensaje": "Usuario registrado",  
        "datos": usuario.dict(exclude={"password"})  # Oculta la contraseña en la respuesta  
    }  
```

7. Probar en Swagger UI
- Visita `http://localhost:8000/docs`.
- Prueba con:

Datos válidos:
```json
{  
  "nombre": "Ana",  
  "email": "ana@example.com",  
  "password": "claveSegura123"  
}  
```

Datos inválidos (ej: email incorrecto):
```json
{  
  "nombre": "A",  
  "email": "no-es-un-email",  
  "password": "123"  
}  
```

FastAPI devolverá errores detallados.

### Ejercicio 2: Modelo de Producto con Restricciones
Crea un modelo para productos con precio positivo y stock no negativo.

1. Definir el modelo
```python
class Producto(BaseModel):  
    nombre: str = Field(min_length=3, max_length=50)  
    precio: float = Field(gt=0, description="El precio debe ser mayor a 0")  
    stock: int = Field(ge=0, description="El stock no puede ser negativo")  
```

2. Endpoint POST
```python
productos_db = []  

@app.get("/lista_productos")
def lista_productos():
    return productos_db

@app.post("/productos/")  
def crear_producto(producto: Producto):  
    productos_db.append(producto.dict())  
    return {"mensaje": "Producto creado", "producto": producto}  
```

3. Probar en Swagger UI
- Visita `http://localhost:8000/docs`.
- Prueba con:

Datos válidos:
```json
{  
  "nombre": "Laptop",  
  "precio": 999.99,  
  "stock": 10  
}  
```

Caso inválido (precio negativo):
```json
{  
  "nombre": "Laptop",  
  "precio": -100,  
  "stock": 10  
}  
```

### Ejercicio 3: Modelos Anidados

Crea un modelo para órdenes de compra que incluya productos y usuarios.

1. Definir modelos anidados
```python
from typing import List

class Orden(BaseModel):  
    usuario: UsuarioRegistro  
    productos: List[Producto]  
    total: float = Field(gt=0)  
```

2. Endpoint POST
```python
@app.post("/ordenes/")  
def crear_orden(orden: Orden):  
    return {  
        "mensaje": "Orden creada",  
        "orden": orden.dict()  
    } 
```

3) Probar en Swagger UI
- Visita `http://localhost:8000/docs`.
- Prueba con:

Probar con datos complejos
```json
{  
  "usuario": {  
    "nombre": "Carlos",  
    "email": "carlos@example.com",  
    "password": "claveSegura456"  
  },  
  "productos": [  
    {  
      "nombre": "Mouse",  
      "precio": 25.99,  
      "stock": 50  
    }  
  ],  
  "total": 25.99  
} 
```

#### Versión Final del Código
```python
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field
from typing import List

class UsuarioRegistro(BaseModel):
    nombre: str = Field(min_length=3, example="Ana")
    email: EmailStr = Field(example="ana@example.com")
    password: str = Field(min_length=8, example="password123")

class Producto(BaseModel):
    nombre: str = Field(min_length=3, max_length=50)
    precio: float = Field(gt=0, description="El precio debe ser mayor a 0")
    stock: int = Field(ge=0, description="El stock no puede ser negativo")

class Orden(BaseModel):
    usuario: UsuarioRegistro
    productos: List[Producto]
    total: float = Field(gt=0)

app = FastAPI()

@app.get("/")
def hola_mundo():
    return {"mensaje": "¡Bienvenido a FastAPI!"}

@app.post("/registro/")
def registrar_usuario(usuario: UsuarioRegistro):
    return {
        "mensaje": "Usuario registrado",
        "datos": usuario.dict(exclude={"password"})  # Oculta la contraseña en la respuesta
    }

productos_db = []

@app.get("/lista_productos")
def lista_productos():
    return productos_db

@app.post("/productos/")
def crear_producto(producto: Producto):
    productos_db.append(producto.dict())
    return {"mensaje": "Producto creado", "producto": producto}

@app.post("/ordenes/")
def crear_orden(orden: Orden):
    return {
        "mensaje": "Orden creada",
        "orden": orden.dict()
    }
```

### Ejercicio extra: 
Añade un campo `categoría` al modelo `Producto` con valores permitidos: `["electrónica", "ropa", "hogar"]`.

## Conclusión
- Creaste modelos Pydantic con validaciones complejas.
- Integraste modelos en endpoints POST.
- Manejaste errores automáticamente.