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

@app.get("/remove/{barcode}")
def remove_from_cart(barcode: str):
    success = cart.remove_item(barcode)
    if success:
        return {"msg": f"{barcode} removed!", "cart": [p.name for p in cart.products]}
    raise HTTPException(status_code=404, detail="Product not found in cart")

@app.get("/delete/cart") 
def delete_cart():
    sucess = cart.delete_cart()
    if sucess:
        return {"msg": "Cart deleted!"}
    raise HTTPException(status_code=404, detail="Cart not found")
