from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Verificar API keys
if not PINECONE_API_KEY:
    print("\n❌ Error: La API key de Pinecone no está configurada.")
    print("\nPor favor sigue estos pasos:")
    print("1. Crea un archivo .env en este directorio (copia .env.example si existe)")
    print("2. Añade tu API key de Pinecone: PINECONE_API_KEY=tu_api_key_aquí")
    print("3. Asegúrate de que la API key sea válida y esté activa")
    print("\nPuedes obtener tu API key en: https://app.pinecone.io/\n")
    sys.exit(1)

app = FastAPI(title="RAG con Pinecone", description="API para RAG utilizando Pinecone como vector database")

INDEX_NAME = "rag-demo"

# Inicializar Pinecone
try:
    from pinecone import Pinecone
    pc = Pinecone(api_key=PINECONE_API_KEY)
    print("✅ Conexión establecida con Pinecone")
except Exception as e:
    print(f"\n❌ Error al conectar con Pinecone: {e}")
    print("Por favor verifica tu API key y conexión a internet.")
    sys.exit(1)

# Inicializar modelo de embeddings
try:
    EMBEDDING_MODEL = SentenceTransformer('all-MiniLM-L6-v2')
    print("✅ Modelo de embeddings cargado correctamente")
except Exception as e:
    print(f"\n❌ Error al cargar el modelo de embeddings: {e}")
    print("Asegúrate de tener instalado sentence-transformers:")
    print("pip install sentence-transformers")
    sys.exit(1)

# Crear índice si no existe
try:
    index_list = [i["name"] for i in pc.list_indexes()]
    
    if INDEX_NAME not in index_list:
        # Versión actualizada con el argumento 'spec' para cuentas gratuitas
        pc.create_index(
            name=INDEX_NAME,
            dimension=EMBEDDING_MODEL.get_sentence_embedding_dimension(),
            spec={"serverless": {"cloud": "aws", "region": "us-east-1"}}
        )
        print(f"✅ Índice '{INDEX_NAME}' creado correctamente")
    else:
        print(f"✅ Índice '{INDEX_NAME}' encontrado")
    
    index = pc.Index(INDEX_NAME)
except Exception as e:
    print(f"\n❌ Error al configurar Pinecone: {e}")
    print("Puedes probar con otro nombre de índice si este está ocupado.")
    # Fallback al servicio de desarrollo
    INDEX_NAME = "rag-demo-dev"
    print(f"Intentando con índice de desarrollo: {INDEX_NAME}")
    try:
        if INDEX_NAME not in [i["name"] for i in pc.list_indexes()]:
            # Versión actualizada con el argumento 'spec' para cuentas gratuitas
            pc.create_index(
                name=INDEX_NAME,
                dimension=EMBEDDING_MODEL.get_sentence_embedding_dimension(),
                spec={"serverless": {"cloud": "aws", "region": "us-east-1"}}
            )
        index = pc.Index(INDEX_NAME)
    except Exception as e2:
        print(f"\n❌ Error al crear índice de desarrollo: {e2}")
        print("Si continúas viendo errores, prueba con la implementación básica sin Pinecone:")
        print("uvicorn main:app --reload")
        sys.exit(1)

# Modelo para agregar documentos
class Document(BaseModel):
    doc_id: str
    text: str

# Modelo para consultas
class Query(BaseModel):
    text: str

@app.post("/add_document")
async def add_document(doc: Document):
    try:
        embedding = EMBEDDING_MODEL.encode(doc.text).tolist()
        index.upsert([(doc.doc_id, embedding, {"text": doc.text})])
        return {"message": "Documento agregado"}
    except Exception as e:
        return {"error": str(e)}

@app.post("/add_file")
async def add_file(file: UploadFile = File(...)):
    try:
        # Crear directorio temporal si no existe
        os.makedirs("documents", exist_ok=True)
        
        # Guardar archivo temporalmente
        file_path = f"documents/{file.filename}"
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Leer contenido del archivo
        with open(file_path, "r") as f:
            text = f.read()
        
        # Generar embedding y guardar en Pinecone
        doc_id = file.filename.replace(".", "_")
        embedding = EMBEDDING_MODEL.encode(text).tolist()
        index.upsert([(doc_id, embedding, {"text": text})])
        
        return {"message": f"Archivo {file.filename} procesado y agregado a Pinecone"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        # Limpiar archivo temporal
        if os.path.exists(file_path):
            os.remove(file_path)

@app.post("/query")
async def rag_query(query: Query):
    try:
        query_embedding = EMBEDDING_MODEL.encode(query.text).tolist()
        results = index.query(vector=query_embedding, top_k=3, include_metadata=True)

        context = " ".join([match["metadata"]["text"] for match in results["matches"] if "metadata" in match])

        return {"answer": f"Respuesta basada en: {context}", "context": context}
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
async def root():
    return {"message": "API de RAG con Pinecone funcionando. Accede a /docs para la documentación."}

@app.on_event("startup")
async def startup_event():
    print("Iniciando servicio RAG con Pinecone...")
    # Puedes inicializar aquí documentos predeterminados si es necesario

if __name__ == "__main__":
    import uvicorn
    print("Iniciando servidor en http://localhost:8001")
    print("Accede a http://localhost:8001/docs para la documentación")
    uvicorn.run(app, host="0.0.0.0", port=8001) 