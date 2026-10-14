
###* 'app.py' Responsabilities: 
# 1. Instantiate FastAPI
# 2. Create all the necesary EndPoints


##* Libraries
# Import the engine that contains the path to the db
from fastapi import FastAPI, status, HTTPException
from database import db_session, Products, Sales, Carts, CartsProducts
from schema import ProductCreate, ProductResponse, SalesCreate, SalesResponse, SalesModify, SalesAssignCarts, CartsCreate, CartsProductsResponse, CartsResponse, CartsProductsCreate
from datetime import datetime
import business_rules as br

##* FastAPI 
app = FastAPI()


##* EndPoints

@app.get("/")
def root():
    return {"message": "Hello!!"}

#* --- PRODUCTOS ---
#* GET /productos
@app.get("/productos", response_model=list[ProductResponse])
def get_products():
    try:
        #? db_session.query(Products) -> Create the SQL Query (SELECT * FROM products)
        #? .all() -> Execute the SQL Query
        return db_session.query(Products).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Un error inesperado ocurrio: {e}")

#* GET /productos/{id}
@app.get("/productos/{id}", response_model=ProductResponse)
def get_product(id: int):
    try:
        product = br.product_exists(db_session, id)
        return product
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Un error inesperado ocurrio: {e}")

#* POST /productos
@app.post("/productos", status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
def create_product(product : ProductCreate):
    try:
        new_product = Products(nombre=product.nombre, precio=product.precio)
        db_session.add(new_product)
        db_session.commit()
        db_session.refresh(new_product) #? updates data so that the id is put correctly
        return new_product
    except Exception as e:
        db_session.rollback() #? if commit gives an error, this revert it
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Un error inesperado ocurrio: {e}")

#* PUT /productos/{id}
@app.put("/productos/{id}", status_code=status.HTTP_200_OK, response_model=ProductResponse)
def update_product(id: int, product: ProductCreate):
    try:
        product_to_update = br.product_exists(db_session, id)

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

#* DELETE /productos/{id}
@app.delete("/productos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int):
    try:
        product_to_delete = br.product_exists(db_session, id)
        br.verify_if_product_is_deletable(db_session, id) #? Important Business Rule

        db_session.delete(product_to_delete)
        db_session.commit()
    except HTTPException:
        raise
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Un error inesperado ocurrio: {e}")





#* --- VENTAS ---
#* GET /ventas
@app.get("/ventas", status_code=status.HTTP_200_OK, response_model=list[SalesResponse])
def get_sales():
    try:
        return db_session.query(Sales).all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Un error inesperado ocurrio: {e}")

#* GET /ventas/{id}
@app.get("/ventas/{id}", status_code=status.HTTP_200_OK, response_model=SalesResponse)
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

#* POST /ventas
@app.post("/ventas", status_code=status.HTTP_201_CREATED, response_model=SalesResponse)
def create_sale(sale: SalesCreate):
    try:
        br.verify_cart_to_sale(db_session, sale.id_carrito) #? Checks: 1. Cart exists, 2. Cart not associated with another sale, 3. Cart in state 'cerrado'

        new_sale = Sales(fecha=sale.fecha, hora=sale.hora, id_carrito=sale.id_carrito)
        db_session.add(new_sale)
        db_session.commit()
        db_session.refresh(new_sale)
        return new_sale
    except HTTPException:
        raise
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ocurrio un error inesperado: {e}")


#* PUT /ventas/{id}
@app.put("/ventas/{id}", status_code=status.HTTP_200_OK, response_model=SalesResponse)
def update_sale(id: int, sale: SalesModify):
    try:
        sale_to_update = db_session.query(Sales).filter(Sales.id == id).first()
        if sale_to_update is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto a actualizar no encontrado!")

        sale_to_update.fecha = sale.fecha
        sale_to_update.hora = sale.hora
        db_session.commit()
        db_session.refresh(sale_to_update)
        return sale_to_update
    except HTTPException:
        raise
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ocurrio un error inesperado: {e}")

#* DELETE /ventas
@app.delete("/ventas/{id}", status_code=status.HTTP_204_NO_CONTENT)
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
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ocurrio un error inesperado: {e}")

#* POST /ventas/{id}/carrito
@app.post("/ventas/{id}/carrito", status_code=status.HTTP_201_CREATED)
def assign_cart_to_sale(id: int, body: SalesAssignCarts):
    try:
        sale = db_session.query(Sales).filter(Sales.id == id).first()
        if sale is None:
            HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venta no encontrada")

        br.verify_cart_to_sale(db_session, body.id_carrito, id_venta_actual=id)

        sale.id_carrito = body.id_carrito
        db_session.commit()
        db_session.refresh(sale)
        return sale
    except HTTPException:
        raise
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ocurrio un error inesperado: {e}")







#* --- Carrito ---
#* GET /carritos
@app.get("/carritos", status_code=status.HTTP_200_OK, response_model=list[CartsResponse])
def get_carts():
    try:
        return db_session.query(Carts).all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ocurrio un error inesperado: {e}")

#* GET /carritos/{id}
@app.get("/carritos/{id}", status_code=status.HTTP_200_OK, response_model=CartsResponse)
def get_cart(id: int):
    try:
        cart = db_session.query(Carts).filter(Carts.id == id).first()
        if cart is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontro el carrito buscado")
        return cart
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ocurrio un error inesperado: {e}")

#* POST /carritos
@app.post("/carritos", status_code=status.HTTP_201_CREATED, response_model=CartsResponse)
def create_cart():
    try:
        time_now = datetime.now()
        new_cart = Carts(estado="abierto", fecha_creacion=time_now.date())

        db_session.add(new_cart)
        db_session.commit()
        db_session.refresh(new_cart)

        return new_cart
    except HTTPException:
        raise
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ocurrio un error inesperado: {e}")


#* PUT /carritos/{id}
@app.put("/carritos/{id}", status_code=status.HTTP_200_OK, response_model=CartsResponse)
def update_cart(id: int, body: CartsCreate):
    try:
        cart = db_session.query(Carts).filter(Carts.id == id).first()
        if cart is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carrito no encontrado")
        
        br.verify_if_cart_is_modifiable(cart)
        
        cart.estado = body.estado
        cart.fecha_creacion = body.fecha_creacion
        
        db_session.commit()
        db_session.refresh(cart)
        return cart
    except HTTPException:
        raise
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ocurrio un error inesperado: {e}")

#* DELETE /carritos/{id}
@app.delete("/carritos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cart(id: int):
    try:
        cart = db_session.query(Carts).filter(Carts.id == id).first()
        if cart is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carrito no encontrado")

        br.verify_if_cart_is_modifiable(cart)
        
        db_session.delete(cart)
        db_session.commit()
    except HTTPException:
        raise
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ocurrio un error inesperado: {e}")

#* POST /carritos/{id}/productos
@app.post("/carritos/{id}/productos", status_code=status.HTTP_201_CREATED, response_model=CartsResponse)
def add_product_to_cart(id: int, body: CartsProductsCreate):
    try:
        cart = db_session.query(Carts).filter(Carts.id == id).first()
        
        if cart is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carrito no encontrado")
        br.verify_if_cart_is_modifiable(cart)
        br.verify_if_cart_is_open(cart)
        br.product_exists(db_session, body.id_producto)

        cart_product = db_session.query(CartsProducts).filter(CartsProducts.id_carrito == id, CartsProducts.id_producto == body.id_producto).first()

        if cart_product is None:
            new_product_to_cart = CartsProducts(cantidad=body.cantidad, id_producto=body.id_producto, id_carrito=id)
            db_session.add(new_product_to_cart)
        else:
            cart_product.cantidad += body.cantidad
        
        db_session.commit()
        db_session.refresh(cart)
        return cart
    except HTTPException:
        raise
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ocurrio un error inesperado: {e}")

#* DELETE /carritos/{id}/productos/{product_id}
@app.delete("/carritos/{id}/productos/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_product_from_cart(id: int, id_producto: int):
    try:
        cart = db_session.query(Carts).filter(Carts.id == id).first()
        if cart is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carrito no encontrado")

        br.verify_if_cart_is_modifiable(cart)
        br.verify_if_cart_is_open(cart)
        br.product_exists(db_session, id_producto)
        cart_product = br.get_product_in_cart(cart, id_producto)

        db_session.delete(cart_product)
        db_session.commit()
    except HTTPException:
        raise
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ocurrio un error inesperado: {e}")