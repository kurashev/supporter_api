from dataclasses import dataclass
from typing import Self

from environs import Env


@dataclass
class AuthConfig:
    secret_key: str
    algorithm: str

    @classmethod
    def compose(cls, env: Env | None = None) -> Self:
        if env is None:
            env = Env()
            env.read_env()
        return cls(
            secret_key=env.str("SECRET_KEY"),
            algorithm=env.str("ALGORITHM")
        )
