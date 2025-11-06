from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.utils import cart as ct
from sqlalchemy.orm import Session
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from app.utils.nutrition_service import NutritionObserver
from app.database import models, schemas
from app.auth import crud
from app.database.database import SessionLocal, engine


app = FastAPI()
cart = ct.Cart()

# Ativação do observer
cart.attach(NutritionObserver())

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/add/{barcode}")
def add_to_cart(barcode: str):
    product = cart.add_product(barcode)
    if product:
        return {"msg": f"{product.code} added!", "cart": [p.name for p in cart.products]} 
    raise HTTPException(status_code=404, detail="Product not found")

@app.get("/cart")
def get_cart():
    list_items = cart.list_items()
    if list_items:
        return {"cart": list_items}
    raise HTTPException(status_code=404, detail="Cart not found")

@app.get("/remove/{barcode}")
def remove_from_cart(barcode: str):
    success = cart.remove_item(barcode)
    if success:
        return {"msg": f"{barcode} removed!", "cart": [p.name for p in cart.products]}
    raise HTTPException(status_code=404, detail="Product not found in cart")

@app.get("/delete/cart") 
def delete_cart():
    success = cart.delete_cart()
    if success:
        return {"msg": "Cart deleted!"}
    raise HTTPException(status_code=404, detail="Cart not found")

#-----------------------------------------------------------------------
# Cria TODAS as 4 tabelas no seu 'cart.db'
models.Base.metadata.create_all(bind=engine)

# --- Dependência do Banco ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
