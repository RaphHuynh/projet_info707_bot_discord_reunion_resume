from pydantic import BaseModel
import datetime


class Resume(BaseModel):
    title: str
    date: datetime.datetime
    duration: datetime.timedelta

    text_sum_up: str

    messages: list
    attendees: list

    admin: int
