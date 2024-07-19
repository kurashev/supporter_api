from fastapi import APIRouter

from src.routes import auth


def register(root_router: APIRouter) -> None:
    for route in (
        auth,
    ):
        root_router.include_router(route.router)
