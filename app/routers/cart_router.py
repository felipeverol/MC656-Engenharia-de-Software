from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.utils import cart as ct
from app.utils.cart import user_carts
from app.utils.nutrition_service import NutritionObserver
from app.auth.jwt_handler import verify_access_token
from app.database.database import get_db
from app.database.crud import create_user_cart
from app.database import schemas

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

@router.post("/save")
def save_cart(cart_name: str, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    cart = get_user_cart(user_id)
    if not cart or cart.list_items()["total_items"] == 0:
        raise HTTPException(status_code=404, detail="Carrinho vazio ou não encontrado")

    cart_data = cart.list_items()["products"]
    cart_schema = schemas.SavedCartCreate(
        name=cart_name,
        cart_data=cart_data
    )

    saved_cart = create_user_cart(db, cart_schema, user_id)
    cart.delete_cart()

    return {"msg": "Cart saved!", "cart": saved_cart}