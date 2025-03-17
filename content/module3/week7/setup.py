#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de configuración para los ejercicios de RAG.
Este script ayuda a configurar el entorno, instalando dependencias y creando el archivo .env.
"""

import os
import sys
import subprocess
import shutil
from getpass import getpass

def print_header(text):
    """Imprime un encabezado formateado."""
    print("\n" + "=" * 60)
    print(f" {text}")
    print("=" * 60)

def print_success(text):
    """Imprime un mensaje de éxito."""
    print(f"✅ {text}")

def print_error(text):
    """Imprime un mensaje de error."""
    print(f"❌ {text}")

def print_info(text):
    """Imprime un mensaje informativo."""
    print(f"ℹ️ {text}")

def check_python_version():
    """Verifica que la versión de Python sea compatible."""
    print_header("Verificando versión de Python")
    major, minor = sys.version_info[:2]
    if major < 3 or (major == 3 and minor < 8):
        print_error(f"Se requiere Python 3.8 o superior. Versión actual: {major}.{minor}")
        return False
    print_success(f"Versión de Python: {major}.{minor}")
    return True

def install_dependencies():
    """Instala las dependencias necesarias."""
    print_header("Instalando dependencias")
    
    dependencies = [
        "langchain-openai",
        "faiss-cpu",
        "langchain-text-splitters",
        "langchain-community",
        "python-dotenv",
        "fastapi",
        "uvicorn",
        "langchain-huggingface",
        "langchain-pinecone",
        "sentence-transformers"
    ]
    
    try:
        for dep in dependencies:
            print_info(f"Instalando {dep}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
        print_success("Todas las dependencias se instalaron correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Error al instalar dependencias: {e}")
        return False

def create_env_file():
    """Crea el archivo .env con las claves API."""
    print_header("Configurando archivo .env")
    
    if os.path.exists(".env"):
        overwrite = input("El archivo .env ya existe. ¿Desea sobrescribirlo? (s/n): ").lower() == 's'
        if not overwrite:
            print_info("Se mantendrá el archivo .env existente")
            return True
    
    # Copiar de .env.example si existe
    if os.path.exists(".env.example"):
        shutil.copy2(".env.example", ".env")
        print_info("Se ha creado .env basado en .env.example")
    else:
        # Crear archivo .env de cero
        with open(".env", "w") as f:
            f.write("# Variables de entorno para ejercicios RAG\n\n")
        print_info("Se ha creado un nuevo archivo .env")
    
    # Solicitar claves API
    print_info("Ingrese sus claves API (deje en blanco para omitir):")
    
    openai_key = getpass("OpenAI API Key: ")
    if openai_key:
        update_env_file("OPENAI_API_KEY", openai_key)
        print_success("API Key de OpenAI configurada")
    else:
        print_info("API Key de OpenAI no configurada")
    
    pinecone_key = getpass("Pinecone API Key (opcional): ")
    if pinecone_key:
        update_env_file("PINECONE_API_KEY", pinecone_key)
        print_success("API Key de Pinecone configurada")
    else:
        print_info("API Key de Pinecone no configurada")
    
    return True

def update_env_file(key, value):
    """Actualiza una clave en el archivo .env."""
    with open(".env", "r") as f:
        lines = f.readlines()
    
    key_exists = False
    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f"{key}={value}\n"
            key_exists = True
            break
    
    if not key_exists:
        lines.append(f"{key}={value}\n")
    
    with open(".env", "w") as f:
        f.writelines(lines)

def check_documents_directory():
    """Verifica y crea el directorio documents si no existe."""
    print_header("Verificando directorio 'documents'")
    
    if not os.path.exists("documents"):
        os.makedirs("documents")
        print_success("Directorio 'documents' creado")
    else:
        print_success("Directorio 'documents' ya existe")
    
    return True

def main():
    """Función principal del script de configuración."""
    print_header("CONFIGURACIÓN DE ENTORNO PARA EJERCICIOS RAG")
    
    if not check_python_version():
        return
    
    if not install_dependencies():
        return
    
    if not create_env_file():
        return
    
    if not check_documents_directory():
        return
    
    print_header("CONFIGURACIÓN COMPLETA")
    print_info("Ahora puede ejecutar los ejercicios:")
    print("  - Ejercicio 1: python rag.py")
    print("  - Ejercicio 2: uvicorn main:app --reload")
    print("  - Ejercicio 3: uvicorn pinecone_main:app --reload --port 8001")
    print("\nPara más información, consulte el archivo README.md")

if __name__ == "__main__":
    main() 