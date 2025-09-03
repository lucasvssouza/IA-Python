# --- Importações de Bibliotecas ---
import os
import tempfile  
import shutil 
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from typing import Optional
# --- Importações de Bibliotecas ---

# --- Importações do Módulo do Projeto ---
from src.backend.agents import verificar_email, Response
# --- Importações do Módulo do Projeto ---

# --- Inicialização da Aplicação ---
app = FastAPI()
# --- Inicialização da Aplicação ---

# --- Configuração de Ficheiros Estáticos (Frontend) ---
STATIC_DIR = os.path.join("src", "frontend")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
# --- Configuração de Ficheiros Estáticos (Frontend) ---

# --- Endpoints da API ---
@app.get("/")
async def read_root():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


@app.post("/verificar-email", response_model=Response)
async def processar_email(
    email_text: Optional[str] = Form(None),
    email_file: Optional[UploadFile] = File(None),
):
    if not email_text and not email_file:
        raise HTTPException(
            status_code=400, detail="Nenhum texto ou ficheiro de e-mail foi enviado."
        )

    resultado: Response

    # Caso 1: O utilizador enviou texto puro.
    if email_text:
        resultado = verificar_email(email_text=email_text)
    
    # Caso 2: O utilizador enviou um ficheiro.
    elif email_file:
        temp_dir = tempfile.mkdtemp()
        temp_file_path = os.path.join(temp_dir, email_file.filename)

        try:
            with open(temp_file_path, "wb") as buffer:
                shutil.copyfileobj(email_file.file, buffer)

            resultado = verificar_email(email_file_path=temp_file_path)
        finally:
            shutil.rmtree(temp_dir)

    if resultado.status == "erro":
        raise HTTPException(status_code=500, detail=resultado.mensagem)

    return resultado
# --- Endpoints da API ---