from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.common.config import Config
from src.common.utilities.generators.holder_generator import session_dependency
from src.infra.database.dao.holder import HolderDAO


def override_dependencies(
        app: FastAPI,
        config: Config,
        session_factory: async_sessionmaker[AsyncSession]
) -> None:
    app.dependency_overrides[Config] = lambda: config
    app.dependency_overrides[async_sessionmaker[AsyncSession]] = lambda: session_factory
    app.dependency_overrides[HolderDAO] = session_dependency(session_factory)
