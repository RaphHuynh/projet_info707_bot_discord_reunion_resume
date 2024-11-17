from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FileRegister(BaseModel):
    id: int
    name: str
    id_message: int
    audio_file_path: str 
    date: datetime