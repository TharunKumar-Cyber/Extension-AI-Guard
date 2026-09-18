from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Extension AI Guard Test Server",
    description="Controlled local server for browser-extension traffic testing.",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "service": "Extension AI Guard Test Server",
        "status": "running",
    }


@app.get("/safe")
def safe():
    return {
        "path": "/safe",
        "type": "safe-test",
    }


@app.get("/suspicious")
def suspicious():
    return {
        "path": "/suspicious",
        "type": "suspicious-test",
    }

@app.post("/malicious-test")
def malicious_test(payload: dict):
    return {
        "path": "/malicious-test",
        "type": "malicious-test",
        "received_bytes": len(str(payload).encode("utf-8")),
        "status": "controlled",
    }