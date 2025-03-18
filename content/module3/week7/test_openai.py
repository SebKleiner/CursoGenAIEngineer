#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para probar directamente la conexión con la API de OpenAI.
"""

import os
from dotenv import load_dotenv
import sys

# Cargar variables de entorno
print("Cargando variables de entorno...")
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("❌ No se encontró la API key de OpenAI en el archivo .env")
    sys.exit(1)

# Verificar si tenemos la biblioteca openai instalada
try:
    from openai import OpenAI
    print("✅ Biblioteca OpenAI encontrada")
except ImportError:
    print("❌ La biblioteca 'openai' no está instalada")
    print("Instalando biblioteca openai...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "openai"])
    from openai import OpenAI
    print("✅ Biblioteca OpenAI instalada")

# Crear un cliente con la API key
print("\nCreando cliente OpenAI con la API key...")
try:
    client = OpenAI(api_key=api_key)
    print("✅ Cliente OpenAI creado correctamente")
except Exception as e:
    print(f"❌ Error al crear cliente OpenAI: {e}")
    sys.exit(1)

# Hacer una prueba simple de la API
print("\nRealizando prueba de conexión con la API de OpenAI...")
try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un asistente útil."},
            {"role": "user", "content": "Hola! Responde solo con una palabra."}
        ]
    )
    print("✅ Conexión exitosa con la API de OpenAI")
    print(f"Respuesta recibida: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ Error al conectar con la API de OpenAI: {e}")
    print("\nPosibles soluciones:")
    print("1. Verifica que la API key sea correcta y esté activa")
    print("2. Asegúrate de tener saldo suficiente en tu cuenta de OpenAI")
    print("3. Comprueba tu conexión a internet")
    print("4. La API key puede tardar unos minutos en activarse después de crearla")
    sys.exit(1)

print("\n✅ Prueba completada con éxito. La API key de OpenAI funciona correctamente.") 