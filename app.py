### 'app.py' Responsabilities: 
# 1. Instantiate FastAPI
# 2. Create all the necesary EndPoints


## Libraries
# Import the engine that contains the path to the db
from fastapi import FastAPI, status, HTTPException
from database import db_session, Products, Sales
from schema import ProductCreate, ProductResponse, SalesCreate, SalesResponse, SalesModify
from datetime import datetime

## FastAPI 
app = FastAPI()


## EndPoints

@app.get("/")
def root():
    return {"message": "Hello!!"}

# --- PRODUCTOS ---
# GET /products
@app.get("/products", response_model=list[ProductResponse])
def get_products():
    try:
        # db_session.query(Products) -> Create the SQL Query (SELECT * FROM products)
        # .all() -> Execute the SQL Query
        return db_session.query(Products).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Un error inesperado ocurrio: {e}")

# GET /products/{id}
@app.get("/products/{id}", response_model=ProductResponse)
def get_product(id: int):
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
def create_product(product : ProductCreate):
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
def update_product(id: int, product: ProductCreate):
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
def delete_product(id: int):
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

# --- VENTAS ---
# GET /sales
@app.get("/sales", status_code=status.HTTP_200_OK, response_model=list[SalesResponse])
def get_sales():
    try:
        return db_session.query(Sales).all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Un error inesperado ocurrio: {e}")

# GET /sales/{id}
@app.get("/sales/{id}", status_code=status.HTTP_200_OK, response_model=SalesResponse)
def get_sale(id: int):
    try:
        sale = db_session.query(Sales).filter(Sales.id == id).first()
        if sale is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venta no encontrada")

        return sale
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Un error inesperado ocurrio: {e}")

# POST /sales
@app.post("/sales", status_code=status.HTTP_201_CREATED, response_model=SalesResponse)
def create_sale(sale: SalesCreate):
    try:
        if sale.cantidad <= 0:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Cantidad Ingresada no valida")
        sale_product = db_session.query(Products).filter(Products.id == sale.id_producto).first()
        if sale_product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID del producto ingresado no encontrado")

        time_now = datetime.now()
        total_price_sale = sale.cantidad * sale_product.precio
        new_sale = Sales(fecha=time_now.date(), hora=time_now.time(), cantidad=sale.cantidad, precio_total=total_price_sale, producto=sale_product)

        db_session.add(new_sale)
        db_session.commit()
        db_session.refresh(new_sale)

        return new_sale
    except HTTPException:
        raise
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ocurrio un error inesperado: {e}")


# PUT /sales/{id}
@app.put("/sales/{id}", status_code=status.HTTP_200_OK, response_model=SalesResponse)
def update_sale(id: int, sale: SalesModify):
    try:
        sale_to_update = db_session.query(Sales).filter(Sales.id == id).first()
        product = db_session.query(Products).filter(Products.id == sale.id_producto).first()
        if (sale_to_update is None) or (product is None):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto a actualizar no encontrado!")

        sale_to_update.cantidad = sale.cantidad
        sale_to_update.id_producto = sale.id_producto
        sale_to_update.fecha = sale.fecha
        sale_to_update.hora = sale.hora
        sale_to_update.precio_total = sale.cantidad * product.precio

        db_session.commit()
        db_session.refresh(sale_to_update)

        return sale_to_update
    except HTTPException:
        raise
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ocurrio un error inesperado: {e}")

# DELETE /sales
@app.delete("/sales/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sale(id: int):
    try:
        sale_to_delete = db_session.query(Sales).filter(Sales.id == id).first()
        if sale_to_delete is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venta a borrar no encontrada!")
        db_session.delete(sale_to_delete)
        db_session.commit()
        
    except HTTPException:
        raise
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ocurrio un error inesperado!")
