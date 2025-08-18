from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers.Traveller.authentication import router as auth_router
import os
from dotenv import load_dotenv
from app.core.logging_setup import setup_logging

load_dotenv()
setup_logging()

app = FastAPI()


allowed_origins = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:5173").split(',')
app.add_middleware(
    CORSMiddleware,
    allow_origins = allowed_origins,
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*'],
    expose_headers=["*"]
)


app.include_router(auth_router)

