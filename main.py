import os
import requests
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

# Configuration Supabase (à adapter avec ta vraie URL et clé)
SUPABASE_URL = "https://wqfzpmnwiqdyvbbrvzhf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndxZnpwbW53aXFkeXZiYnJ2emhmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQwNTM1NDksImV4cCI6MjA2OTYyOTU0OX0.yvJTgSuDYBFB7Gzr_peB5l6r7IAEd81xin8SFm9Hrxg"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_file(file: UploadFile = File(...)):
    content = await file.read()
    filename = file.filename
    size = len(content)

    # Résultat d'analyse fictif pour l'exemple
    result_data = {
        "status": "ok",
        "summary": f"{filename} traité avec succès.",
        "length": size
    }

    # Enregistrement dans Supabase
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "filename": filename,
        "size": size,
        "result": result_data
    }
    response = requests.post(f"{SUPABASE_URL}/rest/v1/analyses", json=data, headers=headers)

    if response.status_code >= 300:
        return {"error": "Échec de l'enregistrement dans Supabase", "detail": response.text}

    return {"message": "Fichier analysé et enregistré", "result": result_data}
