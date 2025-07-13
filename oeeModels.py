from pydantic import BaseModel

class OEE(BaseModel):
    deviceId: str
    location: str
    day: int
    month: int
    year: int