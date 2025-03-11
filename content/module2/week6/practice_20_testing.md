# Clase 20: Introducción al Testing (Parte 1)

# Objetivos: 
- Aprender fundamentos de testing 
- Escribir pruebas unitarias

# ¿Qué es el Testing y Por Qué es Vital?
El testing es el proceso de verificar que tu código funciona como se espera, bajo diferentes escenarios.

## Contexto en APIs:

- Las APIs son la capa crítica entre frontend/backend o entre servicios.

- Un error en un endpoint puede afectar a miles de usuarios o sistemas integrados.

## Beneficios clave:

- Reducción de bugs: Atrapa errores antes de llegar a producción.

- Documentación viva: Los tests muestran cómo se debe usar el API.

- Refactorizar sin miedo: Si los tests pasan, el código sigue funcionando.

## Pirámide de Testing

- Base (más tests):

Unitarias: Prueban funciones o endpoints de forma aislada (ej: GET /items/{id}).

- Medio:

Integración: Verifican interacciones entre componentes (ej: API + base de datos).

- Cúspide (menos tests):

End-to-End (E2E): Simulan flujos completos de usuario (ej: registro → login → compra).

## Herramientas Imprescindibles

### pytest:

- Framework de testing con sintaxis clara y soporte para fixtures.

Ejemplo mínimo:

```python
def test_suma():
    assert 2 + 2 == 4  # Si falla, muestra un error claro
```

### TestClient de FastAPI:

- Simula peticiones HTTP a tu API sin desplegar un servidor real.

- Soporta métodos como .get(), .post(), etc.

Ejemplo:

```python
from fastapi.testclient import TestClient
from main import app  # Importa tu aplicación

client = TestClient(app)

def test_read_item():
    response = client.get("/items/1")
    assert response.status_code == 200
```

## Buenas Prácticas
- Aislamiento: Cada test debe ejecutarse en un entorno limpio (no dependa de otros tests).

- Nombres descriptivos: Usar test_<funcionalidad>_<condición> (ej: test_login_usuario_inexistente).

- Cobertura: Apunta al 70-80% inicialmente (pero prioriza calidad sobre cantidad).

---
# Parte Práctica
## Ejemplo 1:
1. Instalar las dependencias:

```bash
pip install pytest pytest-cov httpx
```
2. Crear un archivo llamado main.py y copiar el siguiente código:

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
```

3. Ejecutar el test
```bash
pytest main.py -v 
```

-v muestra el resultado detallado.

## Ejercicio 2: Separando los tests

En una aplicación real, los test se almacenan en una carpeta diferente al resto de los módulos de la aplicación. 

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

o en el caso de una aplicación más compleja:

```
.
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   └── test_models.py
├── requirements.txt
└── README.md
```

Vamos a usar esta organización haciendo un test para probar un Endpoint GET

**Objetivo:** Validar el comportamiento de GET /items/{id}.

1. Pegá el siguiente código en el archivo main.py:

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()
items_db = [
    {"id": 1, "name": "Laptop"},
    {"id": 2, "name": "Mouse"}
]

@app.get("/items/{item_id}")
def read_item(item_id: int):
    item = next((item for item in items_db if item["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return item
```

2. Pegá el siguiente código en el archivo tests/test_items.py:

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_item_existente():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Laptop"

def test_read_item_no_existente():
    response = client.get("/items/999")
    assert response.status_code == 404
    assert "detail" in response.json()
```

3. Ejecutar el test ejecutando el siguiente comando en la terminal
```bash
pytest
```

o
 
```bash
pytest --cov=app --cov-report=html tests/
```

## Ejecutar Tests
### Método 1 (Interfaz gráfica):

1. Abre el archivo test_items.py.

2. Haz clic en el icono ▶️ verde al lado de una función de test.

3. Selecciona “Run pytest” (PyCharm detecta automáticamente los tests).

### Método 2 (Terminal):

```bash
pytest tests/ -v  # -v para modo detallado
```

2. Analizar Cobertura
Instalar pytest-cov:

```bash
pip install pytest-cov
```

1. Ejecutar tests con coverage:

- En terminal ingresar:

4. Ejecutar los Tests (Windows, Linux, macOS)
Paso 1: Abre una terminal en la raíz del proyecto.
Paso 2: Ejecuta estos comandos:

```bash
# Configurar el entorno (solo una vez por sesión)
export PYTHONPATH=$PYTHONPATH:$(pwd)   # Linux/macOS
set PYTHONPATH=%PYTHONPATH%;%CD%       # Windows

# Ejecutar tests con cobertura
pytest --cov=app --cov-report=html tests/
```

2. Ver reporte: Abre el archivo htmlcov/index.html en tu navegador.


3. Interpretar el Reporte
Porcentaje de cobertura: Verás un % general (ej: 85%) y por archivo.

- Líneas cubiertas: En verde (probadas por tus tests).

- Líneas no cubiertas: En rojo (no probadas).

Haz clic en main.py para ver detalles línea por línea.


### Para practicar:

Si se envía un item_id no numérico FastAPI retorna automáticamente 422 (prueba client.get("/items/abc")).

Generá el test para este caso

## Ejercicio 3: Fixtures para Aislamiento

1. Agregar el siguiente endpoint al main:
```python
@app.post("/items/")
def create_item(item: dict):  # <-- Agrega esta función
    items_db.append(item)
    return {"message": "Item creado", "id": item["id"]}
```

Correr y evaluar el Coverage
```bash
pytest --cov=app --cov-report=html tests/
```

2. Crear tests/conftest.py:

```python
import pytest
from app.main import items_db

@pytest.fixture(autouse=True)
def reset_database():
    original_items = items_db.copy()  # Copia los items originales
    yield  # Aquí se ejecuta el test
    items_db.clear()  # Limpia la base de datos después del test
    items_db.extend(original_items)  # Restaura los items originales

```

3. Crea el siguiente test para POST /items:

```python
def test_create_item():
    # Datos del nuevo item
    new_item = {"id": 3, "name": "Teclado"}

    # Enviar POST al endpoint
    response = client.post("/items/", json=new_item)

    # Verificar respuesta HTTP
    assert response.status_code == 200
    assert response.json() == {"message": "Item creado", "id": 3}

    # Verificar que el item está en la base de datos (vía GET)
    response_get = client.get("/items/3")
    assert response_get.status_code == 200
    assert response_get.json() == new_item
```

### Para practicar:

Ejecuta los tests y verifica en PyCharm que el coverage aumenta.


El archivo tests/conftest.py es un componente clave en proyectos que utilizan pytest para organizar pruebas. Su propósito principal es definir fixtures, configuraciones globales y hooks que pueden ser reutilizados en todos los archivos de prueba del proyecto. 
```
.
├── app/
│   └── main.py
└── tests/
    ├── conftest.py    # Fixtures globales
    └── test_items.py  # Pruebas que usan los fixtures
```

## Ejercicio integrador:

Escribir tests para un nuevo endpoint PUT /items/{item_id} que actualiza un item.

### Requisitos:

- Probar casos donde el item existe/no existe.

- Mockear la función de actualización en la base de datos.
---

# Referencias:
- [Documentación de Testing en FastAPI](https://fastapi.tiangolo.com/tutorial/testing/#extended-fastapi-app-file)
- [Documentación de Testing en PyCharm](https://www.jetbrains.com/help/pycharm/testing.html)