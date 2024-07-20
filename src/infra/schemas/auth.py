from pydantic import EmailStr, Field, SecretStr

from src.infra.schemas.base import BaseSchemaModel


class UserRegister(BaseSchemaModel):
    username: str = Field(min_length=3, max_length=33)
    email: EmailStr = Field()
    password: SecretStr = Field(min_length=5, max_length=33)


class UserAuth(BaseSchemaModel):
    username: str | None = Field(min_length=3, max_length=33)
    password: SecretStr = Field(min_length=5, max_length=33)
