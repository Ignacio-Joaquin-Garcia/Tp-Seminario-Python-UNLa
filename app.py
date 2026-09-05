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

@app.get("/products", response_model=list[ProductResponse])
async def get_products():
    try:
        # db_session.query(Products) -> Create the SQL Query (SELECT * FROM products)
        # .all() -> Execute the SQL Query
        return db_session.query(Products).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {e}")



