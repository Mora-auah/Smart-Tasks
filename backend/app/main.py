from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .db import init_db
from .routers import ai_actions, chat, config, tasks

DIST = Path(__file__).resolve().parents[2] / "frontend" / "dist"


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(title="Smart Tasks", lifespan=lifespan)
for r in (tasks.router, chat.router, ai_actions.router, config.router):
    app.include_router(r)


@app.get("/api/health")
def health():
    return {"ok": True}


# Production-local: serve the built SPA from the same process (client-side routing fallback).
if DIST.exists():
    app.mount("/assets", StaticFiles(directory=DIST / "assets"), name="assets")

    @app.get("/{path:path}", include_in_schema=False)
    def spa(path: str):
        f = DIST / path
        return FileResponse(f if path and f.is_file() else DIST / "index.html")
