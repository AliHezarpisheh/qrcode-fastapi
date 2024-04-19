"""Module defining a FastAPI application with a QR code router."""

from pathlib import Path

from fastapi import FastAPI

from config import setup_logging
from src.routers import qrcode_router

# Logging Configuration.
LOGGING_CONFIG_PATH = Path("logging.toml")
setup_logging(LOGGING_CONFIG_PATH)

# FastAPI instance configurations.
app = FastAPI()

app.include_router(qrcode_router)
