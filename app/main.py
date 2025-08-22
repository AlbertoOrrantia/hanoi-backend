from fastapi import FastAPI

app = FastAPI(title="Hanoi Backend", version="0.0.1")

@app.get("/health")

def health():
    return {"status": "ok"}