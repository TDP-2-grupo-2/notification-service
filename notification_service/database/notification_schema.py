from typing import Optional, Dict
from pydantic import BaseModel

class DeviceBase(BaseModel):
    user_id: int
    token: str

    class Config:
        orm_mode = True