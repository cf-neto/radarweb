from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.backend.website.routes import website_router

from scripts.init_db import init_db


app = FastAPI(title="RadarWeb")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(website_router)

@app.get("/health", summary="Health check da API")
async def health_check():
    return {"status": "ok"}

@app.on_event("startup")
def on_startup():
    init_db()