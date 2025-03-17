from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from rag_handler import OpenAIRAGHandler
import os
from dotenv import load_dotenv
import sys

# Cargar variables de entorno
load_dotenv()

# Verificar que la API key de OpenAI esté configurada correctamente
if not os.getenv("OPENAI_API_KEY"):
    print("\n❌ Error: La API key de OpenAI no está configurada.")
    print("\nPor favor sigue estos pasos:")
    print("1. Crea un archivo .env en este directorio (copia .env.example si existe)")
    print("2. Añade tu API key de OpenAI: OPENAI_API_KEY=tu_api_key_aquí")
    print("3. Asegúrate de que la API key sea válida y esté activa")
    print("\nPuedes obtener tu API key en: https://platform.openai.com/account/api-keys\n")
    sys.exit(1)

app = FastAPI(title="RAG API", description="API para Retrieval Augmented Generation")

try:
    rag = OpenAIRAGHandler()
    print("✅ Conexión establecida con OpenAI")
except Exception as e:
    print(f"\n❌ Error al inicializar el RAG Handler: {e}")
    print("Por favor verifica tu API key y conexión a internet.")
    sys.exit(1)

class QueryRequest(BaseModel):
    question: str

class AddTextRequest(BaseModel):
    text: str

@app.post("/add-text")
async def add_text(request: AddTextRequest):
    try:
        rag.add_text(request.text)
        return {"status": "Texto añadido exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/add-file")
async def add_file(file: UploadFile = File(...)):
    try:
        # Crear directorio si no existe
        os.makedirs("documents", exist_ok=True)
        
        # Guardar archivo temporalmente
        file_path = f"documents/{file.filename}"
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Procesar archivo
        rag.add_file(file_path)
        return {"status": f"Archivo {file.filename} procesado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Limpiar archivo temporal
        if os.path.exists(file_path):
            os.remove(file_path)

@app.post("/ask")
async def ask_question(request: QueryRequest):
    try:
        answer = rag.ask(request.question)
        return {"question": request.question, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "API de RAG funcionando. Accede a /docs para la documentación."}

if __name__ == "__main__":
    import uvicorn
    print("Iniciando servidor en http://localhost:8000")
    print("Accede a http://localhost:8000/docs para la documentación")
    uvicorn.run(app, host="0.0.0.0", port=8000) 