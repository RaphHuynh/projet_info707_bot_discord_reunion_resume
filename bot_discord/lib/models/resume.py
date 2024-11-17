from typing import Optional
from pydantic import BaseModel

class Resume(BaseModel):
    id: int
    text_resume: str
    text_complete: str
    users: Optional[list]
    messages: Optional[list]