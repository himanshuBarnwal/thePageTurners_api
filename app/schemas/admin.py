
from pydantic import BaseModel
        
# schema => req, res validation
class AdminSchema(BaseModel):
    name: str
    email: str
    role: str

    class Config:
        orm_mode = True


class AdminCreateSchema(AdminSchema):
    password: str

    class Config:
        orm_mode = True


class AdminLoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True