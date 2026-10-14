
###* 'models.py' Responsabilities: (Pydanbtic schemes)
# 1. Create the necesary schemas to work with the db

## Libraries
# Import the necessary classes to work with Pydantic Schemas
from pydantic import BaseModel, ConfigDict # Checks Data and Data Structures
from datetime import date, time # Needed Python Data Structures


###* Schemas
##* ---- Products ----
class ProductCreate(BaseModel):
    nombre: str
    precio: float
    class Config:
        from_attributes = True

class ProductResponse(BaseModel):
    id: int
    nombre: str
    precio: float
    #? the class config allows pydantic to read python objects, there are 2 ways to do this:
    #? model_config = {"from_attributes": True}
    class Config:
        from_attributes = True


##* ---- Carts ----
class CartsCreate(BaseModel):
    fecha_creacion: date
    estado: str

class CartsProductsResponse(BaseModel):
    id: int
    producto: ProductResponse
    cantidad: int
    class Config:
        from_attributes = True

class CartsResponse(BaseModel):
    id: int
    fecha_creacion: date
    estado: str
    productos: list[CartsProductsResponse] = []
    class Config:
        from_attributes = True

##* ---- Carts <-> Products ----
class CartsProductsCreate(BaseModel):
    id_producto: int
    cantidad: int

##* ---- Sales ----
class SalesCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True) # Forbids changing the field 'precio_total'
    fecha: date
    hora: time
    id_carrito: int

class SalesResponse(BaseModel):
    id: int
    fecha: date
    hora: time

    carrito: CartsResponse
    precio_total: float

    class Config:
        from_attributes = True

class SalesModify(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)
    fecha: date
    hora: time

class SalesAssignCarts(BaseModel):
    id_carrito: int