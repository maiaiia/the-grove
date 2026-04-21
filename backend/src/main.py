from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from starlette.responses import JSONResponse

from backend.src.router import plant_router, app_router, stats_router, simulation_router
from backend.src.service.plant_validator import PlantValidationError

app = FastAPI(title = "The Grove API")
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parent
IMAGES_DIR = BASE_DIR / "images"

if IMAGES_DIR.exists():
    app.mount("/backend/src/images", StaticFiles(directory=str(IMAGES_DIR)), name="images")

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
app.include_router(simulation_router)

@app.exception_handler(PlantValidationError)
async def plant_validation_exception_handler(request, exception: PlantValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"message": f"Validation Failed: {exception.message}"},
    )


@app.get("/")
def root():
    return {"message": "The Grove's API is working!"}