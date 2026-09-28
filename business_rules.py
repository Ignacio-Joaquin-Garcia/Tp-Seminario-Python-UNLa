from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from database import Products, Sales, Carts, CartsProducts

# Products Rules 
def product_exists(db: Session, id_producto: int) -> Products:
    product = db.query(Products).filter(Products.id == id_producto).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no Encontrado")
    return product
def verify_if_product_is_deletable(db: Session, id_producto: int):
    product_in_cart = db.query(CartsProducts).filter(CartsProducts.id_producto == id_producto).first()
    if product_in_cart is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El producto esta asociado a un carrito")

# Cart Rules
def verify_if_cart_is_open(cart: Carts):
    if cart.estado != "abierto":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Para añadir o eliminar productos el carrido debe estar en estado abierto")

def verify_if_cart_is_modifiable(cart: Carts):
    if cart.venta is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Un carrito asociado a una venta no acepta modificaciones")

def get_product_in_cart(cart: Carts, id_producto: int) -> CartsProducts:
    for product in cart.productos:
        if product.id_producto == id_producto:
            return product
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontro el producto en el carrito")

# Sales Rules
def verify_cart_to_sale(db: Session, id_carrito: int, id_venta_actual: int = None) -> Carts:
    cart = db.query(Carts).filter(Carts.id == id_carrito).first()
    if cart is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carrito no encontrado")
    
    if cart.venta and cart.venta.id != id_venta_actual:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El carrito ya esta asociada a una venta diferente")
    
    if cart.estado != "cerrado":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El carrito debe estar en estado cerrado para realizar esta accion")
    
    return cart