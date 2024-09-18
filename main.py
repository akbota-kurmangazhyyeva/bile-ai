from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.dance_generation import router as dance_router
from app.core.config import settings

app = FastAPI(title="DanceGen API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dance_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)