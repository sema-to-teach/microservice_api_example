from pydantic import BaseModel

class OrderCreate(BaseModel):
    user_id: int
    item: str
    quantity: int

class OrderResponse(BaseModel):
    id: int
    user_id: int
    item: str
    quantity: int

    class Config:
        orm_mode = True