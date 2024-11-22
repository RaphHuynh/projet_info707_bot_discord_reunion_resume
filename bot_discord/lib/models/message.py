import datetime
from typing import Optional
from pydantic import BaseModel


class Message(BaseModel):
    author_id: int

    date: datetime.datetime
    duration: datetime.timedelta

    content: str
    
    
