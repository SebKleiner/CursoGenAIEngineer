# Clase 20: Introducción al Testing (Parte 2)

Hoy vamos a ver los dos tipos de testing que nos faltan:
- Integración: Verifican interacciones entre componentes (ej: API + base de datos).
- End-to-End (E2E): Simulan flujos completos de usuario (ej: registro → login → compra). 

## Pruebas de Integración (FastAPI + Supabase)

Objetivo: Aprender a probar interacciones entre la API y una base de datos real (Supabase).

Introducción a las Pruebas de Integración
¿Qué son?: Pruebas que verifican cómo interactúan múltiples componentes de un sistema (ej: API + base de datos).

¿Por qué son importantes?:

Aseguran que los componentes funcionen correctamente en conjunto.

Detectan errores en flujos complejos (ej: transacciones, conexiones a DB).

Desafíos:

- Configurar entornos de prueba similares a producción.

- Manejar datos de prueba sin afectar la base de datos real.

## Setup Inicial
1. Crear una base de datos en supabase llamada "clase_21" que tenga las siguientes columnas:
- id (int8)
- created_at (timestamptz)
- name (text)

2. Instalar dependencias:

```bash
pip install fastapi supabase pytest httpx python-dotenv passlib python-multipart bcrypt
```

3. Configurar variables de entorno (crear .env):

```python
SUPABASE_URL="tu_url_supabase"
SUPABASE_KEY="tu_clave_supabase"
```
4. Inicializar cliente Supabase (en app/database.py):

```python
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)
```
## Ejercicio 1: Prueba de integración
Objetivo: Probar que un item se crea, lee y elimina en Supabase.

1. Código en FastAPI (app/main.py):
```python
from fastapi import FastAPI, HTTPException
from app.database import supabase
from postgrest.exceptions import APIError 

app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: int):
    response = supabase.table("clase_21").select("*").eq("id", item_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return response.data[0]

@app.post("/items/")
def create_item(item: dict):
    try:
        response = supabase.table("clase_21").insert(item).execute()
        return response.data[0]
    except APIError as e:
        if "23505" in str(e):  # Código de error de duplicidad
            raise HTTPException(
                status_code=409,
                detail="El ítem ya existe"
            )
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor"
        )
```

2. Prueba de Integración (tests/test_integration.py):

```python
from fastapi.testclient import TestClient
from app.main import app
from app.database import supabase
import pytest
import time

client = TestClient(app)

@pytest.fixture(autouse=True)
def cleanup_db():
    # Limpiar ANTES del test (opcional)
    supabase.table("clase_21").delete().neq("id", 0).execute()

    yield  # Aquí se ejecuta el test

    # Limpiar DESPUÉS del test
    supabase.table("clase_21").delete().neq("id", 0).execute()

def test_create_read_item():
    unique_id = int(time.time())

    item_data = {"id": unique_id, "name": "Laptop"}
    response_create = client.post("/items/", json=item_data)

    # Verificar creación
    assert response_create.status_code == 200

    # Verificar lectura
    response_read = client.get(f"/items/{unique_id}")
    assert response_read.status_code == 200
```

Ejecutar 
```bash
pytest --cov=app --cov-report=html tests/
```

**Ejercicio extra:**
Generá un test para el ingreso de un item sin nombre:
```python
invalid_item = {"id": 2}
```
---
## Ejercicio 2: Prueba de End-to-End (E2E)
El test simula un flujo completo de usuario:

- Registro de un usuario.
- Inicio de sesión para obtener un token.
- Creación de un pedido con productos asociados.
- Verificación del pedido en la base de datos.


1. Crea las siguientes bases de datos:
### Tabla `users`
| Nombre de la columna | Tipo de dato    | Restricciones                     |
|----------------------|----------------|----------------------------------|
| `id`                | `BIGSERIAL`     | PRIMARY KEY, AUTO_INCREMENT       |
| `username`          | `TEXT`          | UNIQUE, NOT NULL                  |
| `password`          | `TEXT`          | NOT NULL (almacena hash)          |

### Tabla `orders`
| Nombre de la columna | Tipo de dato    | Restricciones                    |
|----------------------|----------------|----------------------------------|
| `id`                | `BIGSERIAL`     | PRIMARY KEY, AUTO_INCREMENT       |
| `user_id`           | `BIGINT`        | FOREIGN KEY → `users.id`          |
| `product_name`      | `TEXT`          | NOT NULL                          |
| `created_at`        | `TIMESTAMPTZ`   | DEFAULT `now()`                   |



1. Código en FastAPI (app/main.py)
```python
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.database import supabase
from pydantic import BaseModel
from passlib.context import CryptContext
import jwt
import os

app = FastAPI()

# Configuración de seguridad
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "supersecreto"  # ⚠️ Cambiar en producción

# Modelos
class User(BaseModel):
    username: str
    password: str

class Order(BaseModel):
    user_id: int
    product_name: str

# Registro de usuarios
@app.post("/register/")
def register(user: User):
    hashed_password = pwd_context.hash(user.password)
    response = supabase.table("users").insert({"username": user.username, "password": hashed_password}).execute()
    return {"message": "Usuario registrado"}

# Login y generación de token
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    response = supabase.table("users").select("*").eq("username", form_data.username).execute()
    
    if not response.data or not pwd_context.verify(form_data.password, response.data[0]["password"]):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    token = jwt.encode({"sub": form_data.username}, SECRET_KEY, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}

# Crear un pedido (requiere autenticación)
@app.post("/orders/")
def create_order(order: Order, token: str = Depends(oauth2_scheme)):
    response = supabase.table("orders").insert({"user_id": order.user_id, "product_name": order.product_name}).execute()
    return response.data[0]

# Verificar un pedido
@app.get("/orders/{user_id}")
def get_orders(user_id: int):
    response = supabase.table("orders").select("*").eq("user_id", user_id).execute()
    return response.data

```

2. Prueba End-to-End (tests/test_e2e.py)
```python
from fastapi.testclient import TestClient
from app.main import app
from app.database import supabase
import pytest

client = TestClient(app)

@pytest.fixture(autouse=True)
def cleanup_db():
    # Limpiar ANTES del test
    supabase.table("users").delete().neq("id", 0).execute()
    supabase.table("orders").delete().neq("id", 0).execute()
    
    yield  # Ejecutar el test
    
    # Limpiar DESPUÉS del test
    supabase.table("users").delete().neq("id", 0).execute()
    supabase.table("orders").delete().neq("id", 0).execute()

def test_e2e_user_order_flow():
    # 1️⃣ REGISTRAR UN USUARIO
    user_data = {"username": "testuser", "password": "1234"}
    response_register = client.post("/register/", json=user_data)
    assert response_register.status_code == 200

    # 2️⃣ LOGUEARSE Y OBTENER TOKEN
    login_data = {"username": "testuser", "password": "1234"}
    response_login = client.post("/token", data=login_data)
    assert response_login.status_code == 200
    token = response_login.json()["access_token"]
    
    # 3️⃣ CREAR UN PEDIDO
    order_data = {"user_id": 1, "product_name": "Laptop"}
    response_order = client.post("/orders/", json=order_data, headers={"Authorization": f"Bearer {token}"})
    assert response_order.status_code == 200

    # 4️⃣ VERIFICAR QUE EL PEDIDO EXISTE
    response_check = client.get("/orders/1")
    assert response_check.status_code == 200
    assert response_check.json()[0]["product_name"] == "Laptop"

```

3. Ejecución del Test
Para correr la prueba End-to-End:
```bash
pytest --cov=app --cov-report=html tests/
```