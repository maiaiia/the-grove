from contextlib import asynccontextmanager
from pathlib import Path

import strawberry
from fastapi import FastAPI, Depends, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from backend.src.graphql import Query, Mutation
from backend.src.graphql.custom_router import CustomGraphQLRouter
from backend.src.model.database import get_db, engine
from backend.src.model.base import Base
from backend.src.router import simulation_router
from backend.src.router.chat_router import router as chat_router
from backend.src.service import PlantValidationError
from backend.src.service.auth_service import AuthService
from backend.src.model.mongodb import connect_mongo, disconnect_mongo
from .seed_authdb import seed_auth_data

BASE_DIR = Path(__file__).resolve().parent
IMAGES_DIR = BASE_DIR / "images"


@asynccontextmanager
async def lifespan(app: FastAPI):
    seed_auth_data()
    Base.metadata.create_all(bind=engine)
    await connect_mongo()
    print("Startup sequence complete!")
    yield
    await disconnect_mongo()


async def get_context(
        request: Request,
        response: Response,
        db: Session = Depends(get_db)
):
    context = {
        "db": db,
        "request": request,
        "response": response,
        "current_user": None
    }

    access_token = request.cookies.get("access_token")

    if access_token:
        auth_service = AuthService(db)
        current_user = auth_service.get_current_user(access_token)
        context["current_user"] = current_user

    request.state.graphql_context = context
    return context


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = CustomGraphQLRouter(schema, context_getter=get_context)

app = FastAPI(title="The Grove API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://192.168.109.222:5173",
        "http://192.168.109.222:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if IMAGES_DIR.exists():
    app.mount("/backend/src/images", StaticFiles(directory=str(IMAGES_DIR)), name="images")

app.include_router(simulation_router)
app.include_router(graphql_app, prefix="/graphql")
app.include_router(chat_router)


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