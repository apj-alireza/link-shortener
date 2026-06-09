from dataclasses import dataclass


@dataclass
class User:
    user_id: int
    Username: str
    Password: str
    # IsAdmin: bool | None
