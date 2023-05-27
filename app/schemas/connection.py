from pydantic import BaseModel
from datetime import datetime

class ConnectionBase(BaseModel):
    sender_id: int
    receiver_id: int

class ConnectionCreate(BaseModel):
    receiver_id: int
    
class ConnectionUpdate(BaseModel):
    sender_id: int

class Connection(ConnectionBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        orm_mode = True