from fastapi import FastAPI
from app.infrastructure.database import engine, Base
from app.api import auth
from app.api import unidades
from app.api import produtos
from app.api import estoque
from app.api import pedidos
from app.api import fidelidade
from app.api import auditoria

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Raízes do Nordeste API",
    description="API de gestão para a rede de lanchonetes Raízes do Nordeste",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(unidades.router)
app.include_router(produtos.router)
app.include_router(estoque.router)
app.include_router(pedidos.router)
app.include_router(fidelidade.router)
app.include_router(auditoria.router)

@app.get("/")
def raiz():
    return {"status": "ok", "mensagem": "API Raízes do Nordeste funcionando!"}
