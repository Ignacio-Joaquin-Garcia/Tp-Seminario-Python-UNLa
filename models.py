### 'models.py' Responsabilities: (Pydanbtic schemes)
# 1. Create the necesary schemas to work with the db

## Libraries
# Import the necessary classes to work with Pydantic Schemas
from pydantic import BaseModel


## Schemas
# 'POST' ->  Client send something like this: { "nombre": "Mouse", "precio": 1000 }
class ProductCreate(BaseModel):
    nombre: str
    precio: float
# 'GET' -> by parameter {ProductCreate} we pass "nombre" and "precio" and the db adds the new field id
class ProductResponse(BaseModel):
    id: int
    nombre: str
    precio: float
    # the class config allows pydantic to read python objects, there are 2 ways to do this:
    # model_config = {"from_attributes": True}
    class Config:
        from_attributes = True