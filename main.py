from fastapi import FastAPI
from app.api.routers.Traveller.authentication import router as auth_router

app = FastAPI()


app.include_router(auth_router)

