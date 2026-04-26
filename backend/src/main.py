from pathlib import Path

import strawberry
from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from starlette import status
from starlette.responses import JSONResponse

from backend.src.graphql.resolvers import Query, Mutation
from backend.src.router import simulation_router
from backend.src.service.plant_validator import PlantValidationError

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

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

app.include_router(simulation_router)
app.include_router(graphql_app, prefix="/graphql")

@app.exception_handler(PlantValidationError)
async def plant_validation_exception_handler(request, exception: PlantValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"message": f"Validation Failed: {exception.message}"},
    )

@app.api_route("/api/health", methods=["GET", "HEAD"])
def health():
    return {"status": "ok"}
@app.get("/")
def root():
    return {"message": "The Grove's API is working!"}