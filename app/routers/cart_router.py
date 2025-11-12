from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from app.utils import cart as ct
from app.utils.cart import user_carts
from app.utils.nutrition_service import NutritionObserver
from app.auth.jwt_handler import verify_access_token

router = APIRouter(prefix="/cart", tags=["cart"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_user_cart(user_id: int):
    if user_id not in user_carts:
        user_carts[user_id] = ct.Cart()
        user_carts[user_id].attach(NutritionObserver())
    return user_carts[user_id]

def get_current_user_id(token: str = Depends(oauth2_scheme)):
    user_id = verify_access_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    return user_id

### Rotas ###

@router.get("/add/{barcode}")
def add_to_cart(barcode: str, user_id: int = Depends(get_current_user_id)):
    cart = get_user_cart(user_id)
    product = cart.add_product(barcode)
    if product:
        return {"msg": f"{product.code} added!", "cart": [p.name for p in cart.products]}
    raise HTTPException(status_code=404, detail="Product not found")

@router.get("/")
def get_cart(user_id: int = Depends(get_current_user_id)):
    cart = get_user_cart(user_id)
    list_items = cart.list_items()
    if list_items:
        return {"cart": list_items}
    raise HTTPException(status_code=404, detail="Cart not found")

@router.get("/remove/{barcode}")
def remove_from_cart(barcode: str, user_id: int = Depends(get_current_user_id)):
    cart = get_user_cart(user_id)
    success = cart.remove_item(barcode)
    if success:
        return {"msg": f"{barcode} removed!", "cart": [p.name for p in cart.products]}
    raise HTTPException(status_code=404, detail="Product not found in cart")

@router.get("/delete")
def delete_cart(user_id: int = Depends(get_current_user_id)):
    cart = get_user_cart(user_id)
    success = cart.delete_cart()
    if success:
        user_carts.pop(user_id, None)
        return {"msg": "Cart deleted!"}
    raise HTTPException(status_code=404, detail="Cart not found")