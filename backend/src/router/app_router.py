from fastapi import APIRouter

app_router = APIRouter(prefix="/api")
@app_router.get("/health", status_code=200)
@app_router.head("/health", status_code=200)
def health_check():
    return {"status": "online"}