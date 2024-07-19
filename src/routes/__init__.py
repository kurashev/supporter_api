from fastapi import APIRouter


def register(root_router: APIRouter) -> None:
    for route in (

    ):
        root_router.include_router(route.router)
