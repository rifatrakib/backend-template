from fastapi import FastAPI

app: FastAPI = FastAPI()


@app.get("/health")
async def health():
    return {"status": "ok"}
