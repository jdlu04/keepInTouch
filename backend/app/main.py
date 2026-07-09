"""Keep in Touch — FastAPI application entrypoint.

Run locally:  uvicorn app.main:app --reload
Interactive docs:  http://localhost:8000/docs
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routers import auth, connections, interactions, people, reminders

app = FastAPI(
    title="Keep in Touch API",
    version="0.1.0",
    description="Relationship-management backend: contacts, interactions, "
    "reminders, connections, and relationship strength.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok"}


app.include_router(auth.router)
app.include_router(people.router)
app.include_router(interactions.router)
app.include_router(reminders.router)
app.include_router(connections.router)
