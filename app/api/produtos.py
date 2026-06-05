from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.infrastructure.database import get_db
from app.infrastructure.models import Produto
from app.api.deps import require_perfil

router = APIRouter(prefix="/produtos", tags=["Produtos"])

# --- Schemas ---

class ProdutoCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float
    ativo: Optional[bool] = True

class ProdutoUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    preco: Optional[float] = None
    ativo: Optional[bool] = None

class ProdutoResponse(BaseModel):
    id: int
    nome: str
    descricao: Optional[str]
    preco: float
    ativo: bool

    class Config:
        from_attributes = True

# --- Endpoints ---

@router.get("/", response_model=list[ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(Produto).filter(Produto.ativo == True).all()

@router.get("/{produto_id}", response_model=ProdutoResponse)
def buscar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail={
            "error": "PRODUTO_NAO_ENCONTRADO",
            "message": f"Produto {produto_id} não encontrado.",
            "details": [],
            "timestamp": datetime.utcnow().isoformat(),
            "path": f"/produtos/{produto_id}"
        })
    return produto

@router.post("/", response_model=ProdutoResponse, status_code=201)
def criar_produto(
    body: ProdutoCreate,
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("ADMIN", "GERENTE"))
):
    if body.preco <= 0:
        raise HTTPException(status_code=422, detail={
            "error": "PRECO_INVALIDO",
            "message": "O preço deve ser maior que zero.",
            "details": [{"field": "preco", "issue": "deve ser > 0"}],
            "timestamp": datetime.utcnow().isoformat(),
            "path": "/produtos"
        })
    produto = Produto(**body.model_dump())
    db.add(produto)
    db.commit()
    db.refresh(produto)
    return produto

@router.put("/{produto_id}", response_model=ProdutoResponse)
def atualizar_produto(
    produto_id: int,
    body: ProdutoUpdate,
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("ADMIN", "GERENTE"))
):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail={
            "error": "PRODUTO_NAO_ENCONTRADO",
            "message": f"Produto {produto_id} não encontrado.",
            "details": [],
            "path": f"/produtos/{produto_id}"
        })
    for campo, valor in body.model_dump(exclude_unset=True).items():
        setattr(produto, campo, valor)
    db.commit()
    db.refresh(produto)
    return produto

@router.delete("/{produto_id}", status_code=204)
def desativar_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("ADMIN"))
):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail={
            "error": "PRODUTO_NAO_ENCONTRADO",
            "message": f"Produto {produto_id} não encontrado.",
            "details": [],
            "timestamp": datetime.utcnow().isoformat(),
            "path": f"/produtos/{produto_id}"
        })
    produto.ativo = False
    db.commit()
