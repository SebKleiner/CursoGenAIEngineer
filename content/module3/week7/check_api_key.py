#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para verificar la carga correcta de la API key de OpenAI.
"""

import os
from dotenv import load_dotenv

# Intentar cargar variables de entorno
print("Comprobando API key de OpenAI...")
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("\n❌ No se encontró la API key de OpenAI en el archivo .env")
    print("Asegúrate de que:")
    print("1. Exista un archivo .env en esta carpeta")
    print("2. El archivo contenga la línea OPENAI_API_KEY=tu_api_key")
    print("3. No hay espacios alrededor del símbolo =")
else:
    # Mostrar solo los primeros y últimos caracteres para seguridad
    masked_key = f"{api_key[:5]}...{api_key[-4:]}" if len(api_key) > 10 else "***"
    print(f"\n✅ API key encontrada: {masked_key}")
    
    # Verificar formato típico de API key de OpenAI (comienza con sk-)
    if not api_key.startswith("sk-"):
        print("\n⚠️ ADVERTENCIA: La API key no comienza con 'sk-' como es típico en las claves de OpenAI")
        print("Verifica que estés usando una API key válida de OpenAI")
    
    # Verificar si hay espacios en blanco
    if api_key.strip() != api_key:
        print("\n⚠️ ADVERTENCIA: La API key contiene espacios en blanco al principio o al final")
        print("Esto podría causar problemas de autenticación. Edita el archivo .env para removerlos")

# Mostrar el directorio actual para verificar ubicación
print(f"\nDirectorio actual: {os.getcwd()}")
print(f"Buscando archivo .env en: {os.path.abspath('.')}")

# Verificar si el archivo .env existe
if os.path.exists(".env"):
    print("✅ Archivo .env encontrado")
    
    # Mostrar contenido del archivo .env (ocultando la API key completa)
    print("\nContenido del archivo .env (claves enmascaradas):")
    try:
        with open(".env", "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    if "=" in line:
                        key, value = line.split("=", 1)
                        if "key" in key.lower() or "api" in key.lower():
                            # Enmascarar api keys
                            masked_value = f"{value[:5]}...{value[-4:]}" if len(value) > 10 else "***"
                            print(f"{key}={masked_value}")
                        else:
                            print(line)
                    else:
                        print(line)
    except Exception as e:
        print(f"❌ Error al leer el archivo .env: {e}")
else:
    print("❌ No se encontró el archivo .env en este directorio")
    
    # Buscar archivos .env en directorios cercanos
    print("\nBuscando archivos .env en directorios cercanos:")
    for root, dirs, files in os.walk(".."):
        for file in files:
            if file == ".env":
                print(f"  - Encontrado en: {os.path.join(root, file)}") 