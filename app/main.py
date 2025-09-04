from fastapi import FastAPI

# 1. Cria a instância da aplicação que o teste precisa de importar
app = FastAPI()

# 2. Cria a rota raiz que o teste vai chamar
@app.get("/")
def read_root():
    """
    Endpoint raiz para verificar se a API está online.
    """
    return {"status": "ok"}