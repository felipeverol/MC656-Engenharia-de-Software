from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import models
from app.database.database import engine
from app.routers import cart_router, auth_router, email_router

# Inicializa o app
app = FastAPI(title="Carrinho Nutricional")

# Cria as tabelas no banco
models.Base.metadata.create_all(bind=engine)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui os routers
app.include_router(cart_router.router)
app.include_router(auth_router.router)
app.include_router(email_router.router)