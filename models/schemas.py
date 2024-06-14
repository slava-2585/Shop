from datetime import datetime

from pydantic import BaseModel


class Roles(BaseModel):
    id: int
    name: str


class User (BaseModel):
    id: int
    email: str
    password: str
    is_active: bool
    registered_at: datetime
    role_id: Roles
