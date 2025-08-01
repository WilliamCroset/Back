import json
import httpx
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

SUPABASE_URL = "https://wqfzpmnwiqdyvbbrvzhf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndxZnpwbW53aXFkeXZiYnJ2emhmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQwNTM1NDksImV4cCI6MjA2OTYyOTU0OX0.yvJTgSuDYBFB7Gzr_peB5l6r7IAEd81xin8SFm9Hrxg"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_file(file: UploadFile = File(...)):
    content = await file.read()
    filename = file.filename
    size = len(content)

    # Simuler extraction des infos à partir du fichier
    extracted_info = {
        "surface": 132,
        "commune": "Veigy-Foncenex",
        "dpe": "C",
        "terrain": 815
    }

    result_data = {
        "status": "ok",
        "summary": f"{filename} traité avec succès.",
        "extracted_info": extracted_info,
        "length": size
    }

    data_to_save = {
        "filename": filename,
        "size": size,
        "result": result_data
    }

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{SUPABASE_URL}/rest/v1/analyses",
            headers=headers,
            json=data_to_save
        )

    if response.status_code >= 300:
        raise HTTPException(status_code=500, detail=f"Erreur Supabase: {response.text}")

    return {
        "message": "Fichier analysé et enregistré dans Supabase",
        "result": result_data,
        "supabase_response": response.json()
    }
