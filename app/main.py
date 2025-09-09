from fastapi import FastAPI, HTTPException
from app import cart as ct

app = FastAPI()
cart = ct.Cart()

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