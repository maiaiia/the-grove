from pathlib import Path

import strawberry
from fastapi import FastAPI, Depends, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from backend.src.graphql import Query, Mutation, CustomGraphQLRouter
from backend.src.model.database import get_db, engine
from backend.src.model.base import Base
from backend.src.router import simulation_router
from backend.src.service import PlantValidationError
from backend.src.model import Plant, PlantPhoto
from backend.src.service.auth_service import AuthService
from .seed_authdb import seed_auth_data

BASE_DIR = Path(__file__).resolve().parent
IMAGES_DIR = BASE_DIR / "images"


async def get_context(
        request: Request,
        response: Response,
        db: Session = Depends(get_db)
):
    """
    GraphQL context with auth support.
    Extracts user from JWT cookie and handles login/logout cookie operations.
    """
    context = {
        "db": db,
        "request": request,
        "response": response,
        "current_user": None
    }

    # Try to get current user from cookie
    access_token = request.cookies.get("access_token")
    if access_token:
        auth_service = AuthService(db)
        current_user = auth_service.get_current_user(access_token)
        context["current_user"] = current_user

    request.state.graphql_context = context
    return context

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = CustomGraphQLRouter(schema, context_getter=get_context)

app = FastAPI(title="The Grove API")


@app.on_event("startup")
def on_startup():
    # first we need the roles
    seed_auth_data()
    # then the actual data in the database
    """
    print("Dropping data tables...")
    Base.metadata.drop_all(bind=engine)
    """
    print("Creating data tables...")
    Base.metadata.create_all(bind=engine)

    print("Startup sequence complete!")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "*"],
    allow_credentials=True,  # CRITICAL for cookies!
    allow_methods=["*"],
    allow_headers=["*"],
)

if IMAGES_DIR.exists():
    app.mount("/backend/src/images", StaticFiles(directory=str(IMAGES_DIR)), name="images")

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