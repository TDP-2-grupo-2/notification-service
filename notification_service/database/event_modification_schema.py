from pydantic import BaseModel


class Modification(BaseModel):
    message: str
    modifications: dict
    event_id: str
    event_name: str