# Clase 20: Introducción al Testing

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

3. Ejecutar la aplicación

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
│   └── tests/
│       ├── __init__.py
│       ├── test_main.py
│       └── test_models.py
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
from main import app

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
pip install pytest-cov httpx
```

1. Ejecutar tests con coverage:

- En PyCharm: Click derecho en tests/ → “Run pytest with Coverage”.

- En terminal:

```bash
pytest --cov=main --cov-report=html tests/
```

2. Ver reporte: Abre el archivo htmlcov/index.html en tu navegador.


### Para practicar:

¿Qué pasa si se envía un item_id no numérico? FastAPI retorna automáticamente 422 (prueba client.get("/items/abc")).


## Ejercicio 3: Fixtures para Aislamiento
Objetivo: Evitar que los tests compartan estado usando fixtures.

1. Crear tests/conftest.py:

```python
import pytest
from main import items_db

@pytest.fixture(autouse=True)
def reset_database():
    # Guarda el estado original antes de cada test
    original_items = items_db.copy()
    yield  # Aquí se ejecuta el test
    # Restaura la base de datos después del test
    items_db.clear()
    items_db.extend(original_items)
```

2. Crea el siguiente test para POST /items:

```python
def test_create_item():
    item_data = {"id": 3, "name": "Teclado"}
    response = client.post("/items/", json=item_data)
    assert response.status_code == 200
    # Verificar que el item se agregó a la base de datos
    assert any(item["id"] == 3 for item in items_db)
```

### Para practicar:

Ejecuta los tests y verifica en PyCharm que el coverage aumenta.

## Ejercicio integrador:

Escribir tests para un nuevo endpoint PUT /items/{item_id} que actualiza un item.

### Requisitos:

- Probar casos donde el item existe/no existe.

- Mockear la función de actualización en la base de datos.
---

# Referencias:
- [Documentación de FastAPI](https://fastapi.tiangolo.com/tutorial/testing/#extended-fastapi-app-file)
- [Documentación PyCharm](https://www.jetbrains.com/help/pycharm/testing.html)