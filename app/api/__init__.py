# app/api/__init__.py
from .dance_generation import router as dance_router

__all__ = ["dance_router"]