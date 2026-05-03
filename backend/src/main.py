from pathlib import Path

import strawberry
from fastapi import FastAPI, Depends, Request

from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from strawberry.fastapi import GraphQLRouter
from starlette import status
from starlette.responses import JSONResponse

from backend.src.graphql import Query, Mutation
from backend.src.model.database import get_db, engine
from backend.src.model.base import Base
from backend.src.router import simulation_router
from backend.src.service import PlantValidationError

from fastapi.staticfiles import StaticFiles

from backend.src.model import Plant, PlantPhoto

async def get_context(
    request: Request,
    db: Session = Depends(get_db)
):
    return {"db": db, "request": request}

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema, context_getter=get_context)

app = FastAPI(title="The Grove API")

@app.on_event("startup")
def on_startup():
    """
    print("🗑️  Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("✅ All tables dropped!")
    """
    print("🔨 Creating fresh tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created!")

BASE_DIR = Path(__file__).resolve().parent
IMAGES_DIR = BASE_DIR / "images"

if IMAGES_DIR.exists():
    app.mount("/backend/src/images", StaticFiles(directory=str(IMAGES_DIR)), name="images")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "*"],
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