from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.src.router import plant_router, app_router, stats_router

app = FastAPI(title = "The Grove API")
from fastapi.staticfiles import StaticFiles

app.mount("/backend/src/images", StaticFiles(directory="backend/src/images"), name="images")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vue dev server default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(plant_router)
app.include_router(stats_router)
app.include_router(app_router)

@app.get("/")
def root():
    return {"message": "The Grove's API is working!"}