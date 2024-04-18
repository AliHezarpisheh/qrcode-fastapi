from fastapi import FastAPI

from src.routers import qrcode_router

app = FastAPI()

app.include_router(qrcode_router)
