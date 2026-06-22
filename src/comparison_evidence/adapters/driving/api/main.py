from fastapi import FastAPI

app = FastAPI(title="Comparison Evidence Studio")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
