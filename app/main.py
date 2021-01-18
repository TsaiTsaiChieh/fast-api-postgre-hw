
import sys
sys.path.append("/Users/tsaitsaichieh/Desktop/python/fast-api-postgre-hw/")
from typing import Optional
from fastapi import FastAPI
from app import settings
from routes import users

app = FastAPI()

app.include_router(users.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/info")
def info():
    return {"app_name": settings.settings.app_name}
    