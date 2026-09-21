### 'database.py' Responsabilities: (Conection + SQLAlchemy models)
# 1. Create the db engine, 
# 2. Create a Query Session, 
# 3. Create the Tables / Classes

## Libraries -> SQLAlchemy, ORM to communicate between python and SQLite
from sqlalchemy.orm import declarative_base, sessionmaker, relationship 
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Time, ForeignKey


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
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    nombre = Column(String, nullable=False)
    precio = Column(Float, nullable=False)

    ventas = relationship("Sales", back_populates="producto")

class Sales(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    fecha = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    cantidad = Column(Integer, nullable=False)
    
    precio_total = Column(Float, nullable=False)

    id_producto = Column(Integer, ForeignKey("products.id"), nullable=False) # Main Relationship between Products - Sales
    producto = relationship("Products", back_populates="ventas")


## Creation of Tables
Base.metadata.create_all(engine)


## BD Tests
#product_test = Products(nombre="Test", precio=2909.9)
#db_session.add(product_test)
#db_session.commit()