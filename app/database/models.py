from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    # Relação: Um usuário pode ter muitos carrinhos salvos
    carts = relationship("SavedCart", back_populates="owner")


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    barcode = Column(String, index=True)
    name = Column(String, index=True)
    carbo = Column(Float, default=0.0)
    proteina = Column(Float, default=0.0)
    gordura = Column(Float, default=0.0)
    caloria = Column(Float, default=0.0)

    # Relação: Este produto pode estar em muitos 'CartItems'
    cart_items = relationship("SavedCarts", back_populates="product_details")


class SavedCart(Base):
    __tablename__ = "saved_carts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, default="Meu Carrinho")
    
    # Chave estrangeira para o dono do carrinho
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relação: Aponta para o 'User' dono deste carrinho
    owner = relationship("User", back_populates="carts")

