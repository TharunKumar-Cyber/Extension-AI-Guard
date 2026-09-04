from fastapi import FastAPI

app = FastAPI(
    title="Extension AI Guard Test Server",
    description="Controlled local server for browser-extension traffic testing.",
    version="0.1.0",
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
