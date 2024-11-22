from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: int
    discord_tag: str
    avatar: str
    global_name: str
