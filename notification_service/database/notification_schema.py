from pydantic import BaseModel

class DeviceBase(BaseModel):
    device_token: str

    class Config:
        orm_mode = True

class RegisterDevice(BaseModel):
    token: str
    user_id: str

    class Config:
        orm_mode = True
