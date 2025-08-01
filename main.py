from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "API opérationnelle"}

@app.post("/analyze")
async def analyze_file(file: UploadFile = File(...)):
    content = await file.read()
    result = {"filename": file.filename, "size": len(content)}
    return result
