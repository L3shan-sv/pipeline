from fastapi import FastAPI
import socket

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "message": "Pipeline to EKS is working 🚀",
        "hostname": socket.gethostname()
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
