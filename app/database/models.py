from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .database import Base 

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
    # Relação: Um usuário pode ter muitas linhas de "SavedCart"
    carts = relationship("SavedCart", back_populates="owner")


class Product(Base):
    __tablename__ = "products"

    barcode = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    carbo = Column(Float, default=0.0)
    proteina = Column(Float, default=0.0)
    gordura = Column(Float, default=0.0)
    caloria = Column(Float, default=0.0)


class SavedCart(Base):
    __tablename__ = "saved_carts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, default="Meu Carrinho")
    user_id = Column(Integer, ForeignKey("users.id"))
    cart_data = Column(JSON) 
    owner = relationship("User", back_populates="carts")