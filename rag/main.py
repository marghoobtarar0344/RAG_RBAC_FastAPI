from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from routes.rag_router import rag_router
from database.session import init_db
from config.global_variables import (
    CROS_ORIGIN,
    ALLOWED_METHODS,
    ALLOWED_HEADERS,
    TITLE,
    VERSION,
    DESCRIPTION,
    ALLOWED_CREDENTIALS
)


# Initialize FastAPI app
app = FastAPI()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=TITLE,
        version=VERSION,
        description=DESCRIPTION,
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

app.add_middleware(
    CORSMiddleware,
    allow_origins=CROS_ORIGIN,
    allow_credentials=ALLOWED_CREDENTIALS,
    allow_methods=ALLOWED_METHODS,
    allow_headers=ALLOWED_HEADERS,
)


# Initialize Database
@app.on_event("startup")
async def startup_event():
    await init_db()

# Include Routers
app.include_router(rag_router.router, prefix="/rag", tags=["RAG Pipeline"])

# Root Endpoint


@app.get("/")
async def root():
    return {"message": "Welcome to the Async FastAPI RAG System with OSO RBAC"}
