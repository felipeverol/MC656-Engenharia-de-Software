from fastapi import APIRouter, HTTPException
from app.utils import cart as ct
from app.utils.nutrition_service import NutritionObserver

router = APIRouter(prefix="/cart", tags=["cart"])

cart = ct.Cart()
cart.attach(NutritionObserver())

@router.get("/add/{barcode}")
def add_to_cart(barcode: str):
    product = cart.add_product(barcode)
    if product:
        return {"msg": f"{product.code} added!", "cart": [p.name for p in cart.products]} 
    raise HTTPException(status_code=404, detail="Product not found")

@router.get("/")
def get_cart():
    list_items = cart.list_items()
    if list_items:
        return {"cart": list_items}
    raise HTTPException(status_code=404, detail="Cart not found")

@router.get("/remove/{barcode}")
def remove_from_cart(barcode: str):
    success = cart.remove_item(barcode)
    if success:
        return {"msg": f"{barcode} removed!", "cart": [p.name for p in cart.products]}
    raise HTTPException(status_code=404, detail="Product not found in cart")

@router.get("/delete")
def delete_cart():
    success = cart.delete_cart()
    if success:
        return {"msg": "Cart deleted!"}
    raise HTTPException(status_code=404, detail="Cart not found")