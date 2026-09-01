"""FastAPI application factory and router wiring."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import alignment, de, pathways, projects, qc, samples, stages, system
from app.core.config import settings
from app.seed.load import init_db


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=(
            "Read-only FastAPI + SQLite backend for the RNA-seq analysis "
            "platform (GSE52778 demonstration project)."
        ),
        lifespan=None,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    prefix = settings.api_prefix
    app.include_router(system.router, prefix=prefix)
    app.include_router(projects.router, prefix=prefix)
    app.include_router(samples.router, prefix=prefix)
    app.include_router(qc.router, prefix=prefix)
    app.include_router(alignment.router, prefix=prefix)
    app.include_router(stages.router, prefix=prefix)
    app.include_router(de.router, prefix=prefix)
    app.include_router(pathways.router, prefix=prefix)

    return app


# Seed on import so the DB is ready when uvicorn starts.
app = create_app()
init_db()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
