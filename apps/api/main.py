# Auto-generated file
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apps.api.routes.moderation import router as moderation_router
from database.db import engine, Base
from core.logger import logger
from apps.api.middleware.logging import LoggingMiddleware



# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Real Time Content Moderization",
    version="1.0.0",
    description="Find harmful and antilaw contents before pushing to internet"
)


app.include_router(moderation_router)

app.add_middleware(LoggingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Real Time content moderisation api is running",
    }

@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }