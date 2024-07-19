from dataclasses import dataclass


@dataclass
class UserDTO:
    id: int
    username: str
    email: str
    password: str
    is_support: bool
