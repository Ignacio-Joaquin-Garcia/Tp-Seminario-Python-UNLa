### 'models.py' Responsabilities: (Pydanbtic schemes)
# 1. Create the necesary schemas to work with the db

## Libraries
# Import the necessary classes to work with Pydantic Schemas
from pydantic import BaseModel # Checks Data and Data Structures
from datetime import date, time # Needed Python Data Structures


## Schemas

# Products
# 'POST' ->  Client send something like this: { "nombre": "Mouse", "precio": 1000 }
class ProductCreate(BaseModel):
    nombre: str
    precio: float
    class Config:
        from_attributes = True
# 'GET' -> by parameter {ProductCreate} we pass "nombre" and "precio" and the db adds the new field id
class ProductResponse(BaseModel):
    id: int
    nombre: str
    precio: float
    # the class config allows pydantic to read python objects, there are 2 ways to do this:
    # model_config = {"from_attributes": True}
    class Config:
        from_attributes = True

# Sales
# 'POST'
class SalesCreate(BaseModel):
    cantidad: int
    id_producto: int

    class Config:
        from_attributes = True

# 'GET'
class SalesResponse(BaseModel):
    id: int
    fecha: date
    hora: time

    producto: ProductResponse
    cantidad: int

    precio_total: float

    class Config:
        from_attributes = True

# 'PUT'
class SalesModify(BaseModel):
    cantidad: int
    id_producto: int
    fecha: date
    hora: time