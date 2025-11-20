from sqlalchemy.orm import Session
from app.database import models
from app.database import schemas
from app.auth import security

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        name=user.name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, user_login: schemas.UserLogin):
    user = get_user_by_email(db, email=user_login.email)
    if not user:
        return None
    if not security.verify_password(user_login.password, user.hashed_password):
        return None
    return user

# --- Funções do Produto (NOVAS) ---
def get_product_by_barcode(db: Session, barcode: str):
    return db.query(models.Product).filter(models.Product.barcode == barcode).first()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_user_carts(db: Session, user_id: int):
    return db.query(models.SavedCart).filter(models.SavedCart.user_id == user_id).all()

def create_user_cart(db: Session, cart: schemas.SavedCartCreate, user_id: int):
    db_cart = models.SavedCart(
        name=cart.name,
        cart_data=cart.cart_data,
        user_id=user_id
    )
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart

