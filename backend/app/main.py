from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "FastAPI is running!"}

@app.get("/api/v1/health/liveness")
def liveness_check():
    return {"status": "ok"}