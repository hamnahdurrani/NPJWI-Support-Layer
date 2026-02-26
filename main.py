from fastapi import FastAPI
from routers import completions

app = FastAPI(title="Support Layer")

app.include_router(completions.router)

@app.get("/health")
async def health():
    return {"status": "ok"}