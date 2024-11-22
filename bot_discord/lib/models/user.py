from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: int
    discord_tag: str
    avatar: str
    public_flags: int
    global_name: str
    flags: int
    locale: str
    mfa_enabled: bool
