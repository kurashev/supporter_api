from fastapi import APIRouter

from src.routes import auth, user, admin


def register(root_router: APIRouter) -> None:
    for route in (
        auth, user, admin
    ):
        root_router.include_router(route.router)
