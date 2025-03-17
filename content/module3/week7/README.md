# Ejercicios de RAG (Retrieval Augmented Generation)

Este directorio contiene los ejercicios prácticos para aprender sobre RAG (Generación Aumentada por Recuperación).

## Configuración rápida

Para una configuración rápida y sencilla, ejecuta el script de configuración:

```bash
python setup.py
```

Este script:
1. Verifica la versión de Python
2. Instala todas las dependencias necesarias
3. Crea el archivo `.env` y te guía en la configuración de las claves API
4. Prepara el directorio para los archivos

## Configuración manual

Si prefieres configurar el entorno manualmente:

1. Crea un archivo `.env` basado en `.env.example` con tus claves de API:
   ```
   cp .env.example .env
   ```

2. Edita el archivo `.env` y añade tus claves de API para OpenAI y Pinecone.

3. Instala las dependencias necesarias:
   ```bash
   pip install langchain-openai faiss-cpu langchain-text-splitters langchain-community python-dotenv fastapi uvicorn langchain-huggingface langchain-pinecone sentence-transformers
   ```

## Solución de problemas comunes

### Error de API Key

Si ves errores como `AuthenticationError: Incorrect API key provided`, asegúrate de:
1. Haber creado correctamente el archivo `.env`
2. Haber añadido una clave API válida de OpenAI (comienza con `sk-`)
3. Que tu clave API tenga saldo suficiente

### Error al cargar el modelo de embeddings

Si tienes problemas con sentence-transformers, prueba a reinstalarlo:
```bash
pip uninstall -y sentence-transformers
pip install sentence-transformers
```

## Ejercicio 1: RAG Básico

Este ejercicio demuestra cómo implementar un sistema RAG simple utilizando LangChain y FAISS.

1. Revisa el archivo `tu_archivo.txt` que contiene información sobre componentes de agentes autónomos.
2. Ejecuta el script:
   ```bash
   python rag.py
   ```
3. Observa cómo el modelo utiliza la información del archivo para responder a la pregunta.

### Ejercicio Extra:
1. Modifica `tu_archivo.txt` añadiendo nueva información.
2. Modifica `rag.py` para cambiar la pregunta a algo relacionado con la nueva información.
3. Modifica `rag.py` para preguntar algo que no esté en el archivo y observa la respuesta.

## Ejercicio 2: RAG con FastAPI

Este ejercicio implementa un servicio API para RAG utilizando FastAPI.

1. Ejecuta el servidor:
   ```bash
   uvicorn main:app --reload
   ```

2. Accede a `http://localhost:8000/docs` para ver la documentación interactiva de la API.

3. Prueba los endpoints:
   - `/add-text`: Añade texto directamente a la base de conocimiento.
   - `/add-file`: Sube un archivo (txt o pdf) para añadirlo a la base de conocimiento.
   - `/ask`: Realiza consultas sobre la información almacenada.

## Ejercicio 3: RAG con Pinecone

Este ejercicio implementa RAG utilizando Pinecone como vector database.

1. Asegúrate de tener una cuenta en Pinecone y añade tu API key al archivo `.env`.

2. Ejecuta el servidor:
   ```bash
   uvicorn pinecone_main:app --reload --port 8001
   ```

3. Accede a `http://localhost:8001/docs` para ver la documentación interactiva de la API.

4. Prueba los endpoints:
   - `/add_document`: Añade texto directamente a Pinecone.
   - `/add_file`: Sube un archivo para añadirlo a Pinecone.
   - `/query`: Realiza consultas sobre la información almacenada.

## Estructura de archivos

```
.
├── .env.example            # Plantilla para variables de entorno
├── setup.py                # Script de configuración automática
├── rag.py                  # Ejercicio 1: RAG básico
├── main.py                 # Ejercicio 2: API con FastAPI
├── pinecone_main.py        # Ejercicio 3: API con Pinecone
├── rag_handler.py          # Clase para manejar operaciones RAG
├── README.md               # Este archivo
├── tu_archivo.txt          # Datos de ejemplo
└── documents/              # Directorio para archivos subidos
```

## Notas importantes

- Los ejemplos utilizan OpenAI para embeddings y generación de texto. Asegúrate de tener saldo suficiente.
- El ejercicio con Pinecone requiere una cuenta gratuita en Pinecone.
- Estos ejercicios son para fines educativos y pueden requerir ajustes para uso en producción.