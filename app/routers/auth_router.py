# app/routers/auth_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.database import crud, schemas, database
from app.auth import jwt_handler, security

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# --- Dependência do banco ---
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Registrar novo usuário ---
@router.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado.")
    new_user = crud.create_user(db, user)
    return new_user

# --- Login e geração de token ---
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas.")
    token = jwt_handler.create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

# --- Retornar dados do usuário autenticado ---
@router.get("/me", response_model=schemas.User)
def get_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = jwt_handler.verify_access_token(token)
    user = db.query(crud.models.User).filter(crud.models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return user
