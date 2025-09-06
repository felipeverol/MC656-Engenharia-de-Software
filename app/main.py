from fastapi import FastAPI, HTTPException
import app.cart as ct

app = FastAPI()
cart = ct.Cart()

@app.get("/add/{barcode}")
def add_to_cart(barcode: str):
    product = cart.add_product(barcode)
    if product:
        return {"msg": f"{product.code} added!", "cart": [p.name for p in cart.products]} 
    raise HTTPException(status_code=404, detail="Product not found")