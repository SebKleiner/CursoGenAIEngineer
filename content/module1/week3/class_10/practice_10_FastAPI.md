# FastAPI y Pydantic - Parte 2
Cómo hacer una aplicación con FastAPI (Paso a paso)

1) Importar FastAPI
```python
from fastapi import FastAPI
```

2) Crear la Instancia FasAPI
```python
app = FastAPI()
```
La instancia quedará guardada en la variable app y con esta variable vamos a interactar para crear la API


3) Crear el URL o el endpoint
Podemos crearlo con Operaciones o métodos.

En la clase 9 vimos los siguientes Endpoints:

- GET: Para leer datos
- POST: Para crear datos

Hoy vamos a ver más

```python
@app.get("/")

```

4) Definir la función que se va a ejecutar en el endpoint
```python
def hola_mundo():
    return {"message": "Hello World"}
```

Dentro de la función podemos devolver valores (str, int, etc) o también podemos devolver elementos como diccionarios o listas. 

5) Ejecutar la aplicación

---
Uso de async def en FastAPI

FastAPI permite definir funciones asíncronas usando async def, lo que mejora la eficiencia cuando se manejan múltiples solicitudes concurrentemente. Esto es útil en operaciones de entrada/salida (E/S) como consultas a bases de datos, llamadas a APIs externas o lectura/escritura de archivos.

¿Por qué usar async def?

Normalmente, en Python, las funciones se ejecutan de manera secuencial. Si una función tarda mucho tiempo en completarse (por ejemplo, al consultar una base de datos), el servidor podría quedar bloqueado hasta que termine.

Con async def, FastAPI puede manejar otras solicitudes mientras espera la respuesta de la operación lenta, mejorando el rendimiento del sistema.

```python
from fastapi import FastAPI
import asyncio

app = FastAPI()

@app.get("/")
async def read_root():
    await asyncio.sleep(2)  # Simula una operación lenta
    return {"message": "Hola, mundo!"}
```
Explicación del código

1. `async def read_root()`: Define una función asíncrona que puede ejecutarse sin bloquear el servidor.

2. `await asyncio.sleep(2)`: Simula una operación de E/S que tarda 2 segundos.

3. Mientras `asyncio.sleep(2)` está en curso, FastAPI puede manejar otras solicitudes.

Cuándo usar async def

Usá async def cuando:

- Hacés consultas a bases de datos asíncronas.

- Realizás peticiones HTTP a otras APIs.

- Trabajás con archivos de manera asíncrona.

No es necesario usar async def si tu código solo realiza operaciones rápidas y síncronas, como cálculos matemáticos o procesamiento en memoria.


---
# Manejo de excepciones con `raise` en FastAPI

## 1. ¿Qué hace `raise` en Python?
`raise` es una palabra clave en Python que permite generar errores manualmente. Cuando se usa, la ejecución del programa se detiene y se muestra un mensaje de error.

## 2. `raise HTTPException` en FastAPI
FastAPI utiliza `HTTPException` para manejar errores HTTP de forma estructurada. Esto permite devolver respuestas con códigos de estado específicos y mensajes personalizados cuando ocurre un error en una solicitud.

Si una condición no deseada ocurre en una función de FastAPI, se puede lanzar `HTTPException` para indicar que la solicitud no es válida.

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/users/{user_id}")
def read_user(user_id: int):
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="El ID de usuario debe ser mayor a 0")
    return {"user_id": user_id}

```
📌 Si alguien intenta acceder a /users/0, devuelve un 400 Bad Request con el mensaje "El ID de usuario debe ser mayor a 0".

## 3. Otras excepciones útiles en FastAPI

### 🔹 `RequestValidationError`
Se lanza automáticamente cuando los datos enviados en la solicitud no cumplen con el esquema esperado. Esto es útil para validar datos de entrada y asegurarse de que sean correctos antes de procesarlos.

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    age: int

@app.post("/users/")
def create_user(user: User):
    return user

```
📌 Si alguien envía { "name": "Juan", "age": "hola" }, FastAPI responde con un 422 Unprocessable Entity porque "hola" no es un número.

### 🔹 `StarletteHTTPException`
Es una excepción interna de Starlette (el framework en el que se basa FastAPI) que FastAPI maneja automáticamente. Se usa principalmente para gestionar errores de rutas y respuestas HTTP.

```python
from fastapi import FastAPI
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": "Ruta no encontrada o método incorrecto"},
    )
```
📌 Si alguien intenta acceder a una ruta inválida, en lugar de devolver un error genérico, el sistema mostrará "Ruta no encontrada o método incorrecto".

### 🔹 `ValidationError`
Proviene de **Pydantic** y se usa para validar datos estructurados. Se lanza cuando los datos proporcionados no cumplen con las restricciones definidas en los modelos de datos.

```python
from pydantic import BaseModel, ValidationError

class User(BaseModel):
    name: str
    age: int

try:
    user = User(name="Juan", age="no es un número")
except ValidationError as e:
    print(e)
```
📌 Esto imprimirá un error detallado indicando que "no es un número" no es un valor válido para age.

## 4. Cuándo usar cada excepción

| Excepción                | Uso principal |
|--------------------------|--------------|
| `HTTPException`          | Para manejar errores HTTP personalizados en los endpoints. |
| `RequestValidationError` | Para indicar que los datos enviados en una solicitud no cumplen con los requisitos esperados. |
| `StarletteHTTPException` | Para gestionar errores internos de Starlette, como rutas inexistentes. |
| `ValidationError`        | Para validar datos con Pydantic antes de procesarlos. |

El uso correcto de estas excepciones permite que las aplicaciones FastAPI manejen errores de manera clara y eficiente.



---
## Otros Endpoints:

1. Endpoint PUT (Actualizar un recurso existente)
Descripción: Crea un endpoint PUT que permita actualizar un recurso existente (por ejemplo, un usuario) en una lista o base de datos simulada.

Requisitos:

- Usa un modelo Pydantic para validar los datos de entrada.

- Si el recurso no existe, devuelve un error 404.

- Si el recurso existe, actualízalo y devuelve el recurso actualizado.

Ejemplo:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    age: int

users = [
    User(id=1, name="Alice", age=25),
    User(id=2, name="Bob", age=30),
]

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, updated_user: User):
    for index, user in enumerate(users):
        if user.id == user_id:
            users[index] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail="User not found")
```

2. Endpoint DELETE (Eliminar un recurso)
Descripción: Crea un endpoint DELETE que permita eliminar un recurso (por ejemplo, un usuario) de una lista o base de datos simulada.

Requisitos:

- Si el recurso no existe, devuelve un error 404.

- Si el recurso existe, elimínalo y devuelve un mensaje de éxito.

Ejemplo:

```python
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for index, user in enumerate(users):
        if user.id == user_id:
            users.pop(index)
            return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")  
```

3. Endpoint PATCH (Actualización parcial de un recurso)
Descripción: Crea un endpoint PATCH que permita actualizar parcialmente un recurso (por ejemplo, un usuario).

Requisitos:

- Usa un modelo Pydantic con campos opcionales para validar los datos de entrada.

- Si el recurso no existe, devuelve un error 404.

- Si el recurso existe, actualiza solo los campos proporcionados.

Ejemplo:

```python
class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None

@app.patch("/users/{user_id}", response_model=User)
def partial_update_user(user_id: int, updated_data: UserUpdate):
    for user in users:
        if user.id == user_id:
            if updated_data.name is not None:
                user.name = updated_data.name
            if updated_data.age is not None:
                user.age = updated_data.age
            return user
    raise HTTPException(status_code=404, detail="User not found")
```

---
Ejercicio de cierre:
Incorporá a la aplicación que creaste en la clase 9 los siguientes elementos:
1) Probá la eficiencia de tu código usando `async`
2) Un `raise HTTPException` 
3) Un nuevo tipo de Endpoint