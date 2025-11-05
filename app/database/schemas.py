from pydantic import BaseModel, EmailStr
from typing import List, Optional

class ProductBase(BaseModel):
    name: str
    carbo: float = 0
    proteina: float = 0
    gordura: float = 0
    caloria: float = 0

class ProductCreate(ProductBase):
    barcode: str # Para criar, precisamos do barcode

class Product(ProductBase):
    barcode: str # Para ler, também mostramos o barcode

    class Config:
        orm_mode = True


class CartItemBase(BaseModel):
    quantity: int = 1

class CartItemCreate(CartItemBase):
    product_barcode: str # Para criar, precisamos do barcode

class CartItem(CartItemBase):
    id: int
    product_details: Product # Aninha os detalhes completos do produto

    class Config:
        orm_mode = True


class SavedCartBase(BaseModel):
    name: str = "Meu Carrinho"

class SavedCartCreate(SavedCartBase):
    pass

class SavedCart(SavedCartBase):
    id: int
    user_id: int
    items: List[CartItem] = [] # Mostra a lista de itens do carrinho

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    # Modificado para usar o novo schema de Carrinho
    carts: List[SavedCart] = [] 

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str