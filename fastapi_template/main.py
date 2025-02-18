from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from fast_api.api import api

app = FastAPI()

# Include routers
app.include_router(api.router)

# CORS middleware example
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)