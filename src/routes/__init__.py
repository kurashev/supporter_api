from fastapi import APIRouter

from src.routes import auth, user, admin, ticket


def register(root_router: APIRouter) -> None:
    for route in (
        auth, user, admin, ticket
    ):
        root_router.include_router(route.router)
