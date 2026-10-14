
# *  'database.py' Responsabilities: (Conection + SQLAlchemy models)
# 1. Create the db engine, 
# 2. Create a Query Session, 
# 3. Create the Tables / Classes

## Libraries -> SQLAlchemy, ORM to communicate between python and SQLite
from sqlalchemy.orm import declarative_base, sessionmaker, relationship 
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Time, ForeignKey
import os

## Creation of the SQLite Engine
# echo=true parameter show us in the terminal the sql instructions that are running 
engine = create_engine('sqlite:///database.db', echo=True)
# the base is a special class used to create tables
Base = declarative_base()


## Session Configuration
# Sessions Factory
SessionFactory = sessionmaker(bind=engine)
# Specific session
db_session = SessionFactory() 


## Tables
class Products(Base):
    __tablename__ = 'products'
    # Data
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    nombre = Column(String, nullable=False)
    precio = Column(Float, nullable=False)
    # Relation Data
    carrito_producto = relationship("CartsProducts", back_populates="producto")
    #! ventas = relationship("Sales", back_populates="producto")

class Sales(Base):
    __tablename__ = 'sales'
    # Data
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    fecha = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    # Relation Data
    id_carrito = Column(Integer, ForeignKey("carts.id"), nullable=False, unique=True)
    carrito = relationship("Carts", back_populates="venta")

    @property
    def precio_total(self) -> float:
        return sum(cp.cantidad * cp.producto.precio for cp in self.carrito.productos)

    

class Carts(Base):
    __tablename__ = 'carts'
    # Data
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    fecha_creacion = Column(Date, nullable=False)
    estado = Column(String, nullable=False)
    # Relation Data
    productos = relationship("CartsProducts", back_populates="carritos", cascade="all, delete-orphan")
    venta = relationship("Sales", back_populates="carrito", uselist=False) # By default 'relationship' is for 1:n with uselist=False we map to 1:1

class CartsProducts(Base):
    __tablename__ = 'carts_products'
    # Data
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    cantidad = Column(Integer, nullable=False)
    # Relation Data
    id_producto = Column(Integer, ForeignKey("products.id"), nullable=False)
    producto = relationship("Products", back_populates="carrito_producto")
    id_carrito = Column(Integer, ForeignKey("carts.id"), nullable=False)
    carritos = relationship("Carts", back_populates="productos")
    

## Creation of Tables
print(os.path.abspath("database.db"))
DB_FILE = "database.db"
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
Base.metadata.create_all(engine)


##// BD Tests
#//product_test = Products(nombre="Test", precio=2909.9)
#//db_session.add(product_test)
#//db_session.commit()