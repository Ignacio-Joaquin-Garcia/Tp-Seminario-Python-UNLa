### 'app.py' Responsabilities: 
# 1. Instantiate FastAPI
# 2. Create all the necesary EndPoints


## Libraries
# Import the engine that contains the path to the db
from fastapi import FastAPI, status, HTTPException
from database import db_session, Products
from models import ProductCreate, ProductResponse


## FastAPI 
app = FastAPI()


## EndPoints

@app.get("/")
async def root():
    return {"message": "Hello!!"}

# GET /products
@app.get("/products", response_model=list[ProductResponse])
async def get_products():
    try:
        # db_session.query(Products) -> Create the SQL Query (SELECT * FROM products)
        # .all() -> Execute the SQL Query
        return db_session.query(Products).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Un error inesperado ocurrio: {e}")

# GET /products/{id}
@app.get("/products/{id}", response_model=ProductResponse)
async def get_product(id: int):
    try:
        product = db_session.query(Products).filter(Products.id == id).first()
        if product == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
        return product
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Un error inesperado ocurrio: {e}")

# POST /products
@app.post("/products", status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
async def create_product(product : ProductCreate):
    try:
        new_product = Products(nombre=product.nombre, precio=product.precio)
        db_session.add(new_product)
        db_session.commit()
        db_session.refresh(new_product) # updates data so that the id is put correctly
        return new_product
    except Exception as e:
        db_session.rollback() # if commit gives an error, this revert it
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Un error inesperado ocurrio: {e}")

# PUT /products/{id}
@app.put("/products/{id}", status_code=status.HTTP_200_OK, response_model=ProductResponse)
async def update_product(id: int, product: ProductCreate):
    try:
        product_to_update = db_session.query(Products).filter(Products.id == id).first()
        if product_to_update is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
        product_to_update.nombre = product.nombre
        product_to_update.precio = product.precio
        db_session.commit()
        db_session.refresh(product_to_update)
        return product_to_update
    except HTTPException:
        raise
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Un error inesperado ocurrio: {e}")

# DELETE /products/{id}
@app.delete("/products/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(id: int):
    try:
        product_to_delete = db_session.query(Products).filter(Products.id == id).first()
        if product_to_delete is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
        db_session.delete(product_to_delete)
        db_session.commit()
    except HTTPException:
        raise
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Un error inesperado ocurrio: {e}")
