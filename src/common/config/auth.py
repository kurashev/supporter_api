from dataclasses import dataclass
from typing import Self

from environs import Env


@dataclass
class AuthConfig:
    jwt_secret_key: str
    jwt_refresh_secret_key: str
    algorithm: str

    @classmethod
    def compose(cls, env: Env | None = None) -> Self:
        if env is None:
            env = Env()
            env.read_env()
        return cls(
            jwt_secret_key=env.str("JWT_SECRET_KEY"),
            jwt_refresh_secret_key=env.str("JWT_REFRESH_SECRET_KEY"),
            algorithm=env.str("ALGORITHM")
        )
