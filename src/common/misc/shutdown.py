from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine


def register_shutdown_events(app: FastAPI, db_engine: AsyncEngine) -> None:
    app.add_event_handler('shutdown', db_engine.dispose)