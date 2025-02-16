# Introducción a FastAPI  - Práctica

## Descripción

En esta guía, exploraremos los fundamentos de FastAPI, un framework moderno para construir APIs en Python, y Pydantic, una biblioteca para la validación de datos. Aprenderemos cómo estas herramientas trabajan juntas para crear aplicaciones robustas y eficientes, con énfasis en su integración y ventajas clave.

## Objetivos

- Entender qué es FastAPI y sus casos de uso.
- Familiarizarse con conceptos básicos como rutas, parámetros y decoradores.
- Preparar el entorno de desarrollo para comenzar a programar.

Cada ejercicio introduce nuevos conceptos y herramientas clave para desarrollar chatbots cada vez más sofisticados, permitiéndote experimentar con el potencial de los modelos de lenguaje en aplicaciones del mundo real.

Asegúrate de tener un entorno de programación adecuado y de seguir cada paso detalladamente para obtener los mejores resultados. ¡Manos a la obra!

## Actividades

### Ejercicio 1: Configuración Inicial

1. Crea un archivo main.py en PyCharm.

2. Instala las dependencias:

```bash
pip install fastapi uvicorn
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

5. Probar el endpoint
Visita `http://localhost:8000` en tu navegador.

Deberías ver:
```json
{"mensaje": "¡Bienvenido a FastAPI!"}  
```

**Explicación**
- `@app.get("/")`: Define un endpoint GET en la ruta raíz.
- FastAPI convierte automáticamente el diccionario a JSON.

### Ejercicio 2: Endpoint con Parámetro de Ruta
Crearemos un endpoint que reciba un nombre por la URL y devuelva un saludo personalizado.

1) Agregar al código `main.py`
```python
@app.get("/saludar/{nombre}")  
def saludar(nombre: str):  
    return {"mensaje": f"Hola, {nombre}!"}  
```
2) Probar el endpoint
- Visita `http://localhost:8000/saludar/Ana`
- Resultado esperado:
```json
{"mensaje": "Hola, Ana!"}  
```

**Explicación**

`{nombre}` es un parámetro de ruta. FastAPI lo convierte automáticamente a `str`.

### Ejercicio 3: Endpoint para Verificar Par/Impar
Crearemos un endpoint que reciba un número por la ruta y determine si es par o impar.

1) Agregar al código `main.py`
```python
@app.get("/par-impar/{numero}")  
def verificar_paridad(numero: int):  
    if numero % 2 == 0:  
        return {"resultado": "par"}  
    else:  
        return {"resultado": "impar"}  
```
2) Probar el endpoint
- Visita `http://localhost:8000/par-impar/7`
- Resultado esperado:
```json
{"resultado": "impar"}  
```
Prueba con otro número: `http://localhost:8000/par-impar/10` → `{"resultado": "par"}`.


3) Probar en Swagger UI
Visita `http://localhost:8000/docs`.

- Busca el endpoint `GET /par-impar/{numero}`.

- Haz clic en "Try it out", ingresa un número y ejecuta.

- Ejemplo:
```json
{  
  "numero": 15  
}  
```

- Respuesta esperada:
```json
{"resultado": "impar"}  
```

**Explicación**

- `{numero}` es un parámetro de ruta que FastAPI convierte automáticamente a entero.

- La operación `numero % 2` devuelve el resto de la división por 2. Si es `0`, el número es par.


#### Relación con Validación de Datos
FastAPI automáticamente valida que numero sea un entero. Si se ingresa un valor no numérico (ej: /par-impar/abc), la API devolverá un error descriptivo:

```json
{  
  "detail": [  
    {  
      "type": "int_parsing",  
      "loc": ["path", "numero"],  
      "msg": "Input should be a valid integer, unable to parse string as an integer",  
      "input": "abc"  
    }  
  ]  
}  
```

#### Versión Final del Código
```python
from fastapi import FastAPI  

app = FastAPI()  

@app.get("/")  
def hola_mundo():  
    return {"mensaje": "¡Bienvenido a FastAPI!"}  

@app.get("/saludar/{nombre}")  
def saludar(nombre: str):  
    return {"mensaje": f"Hola, {nombre}!"}  

@app.get("/par-impar/{numero}")  
def verificar_paridad(numero: int):  
    return {"resultado": "par" if numero % 2 == 0 else "impar"}  
```

### Ejercicio extra: 
Modifica el endpoint para que también acepte números negativos y devuelva un mensaje personalizado (ej: "par-negativo" o "impar-negativo").

## Conclusión

FastAPI y Pydantic representan un estándar moderno para el desarrollo de APIs en Python, combinando rendimiento, seguridad y facilidad de uso. Estas herramientas son esenciales para construir aplicaciones escalables, especialmente en entornos donde la validación de datos y la documentación son críticas (ej: microservicios, integraciones con frontend).