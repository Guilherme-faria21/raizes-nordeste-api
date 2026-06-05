from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.infrastructure.database import get_db
from app.infrastructure.models import Estoque, MovimentacaoEstoque, Unidade, Produto
from app.application.auditoria_service import registrar as registrar_auditoria
from app.api.deps import require_perfil

router = APIRouter(prefix="/estoque", tags=["Estoque"])

# --- Schemas ---

class EntradaEstoque(BaseModel):
    unidade_id: int
    produto_id: int
    quantidade: int
    motivo: Optional[str] = "Entrada manual"

class EstoqueResponse(BaseModel):
    id: int
    unidade_id: int
    produto_id: int
    quantidade: int

    class Config:
        from_attributes = True

class MovimentacaoResponse(BaseModel):
    id: int
    estoque_id: int
    tipo: str
    quantidade: int
    motivo: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# --- Endpoints ---

@router.get("/{unidade_id}", response_model=list[EstoqueResponse])
def listar_estoque_unidade(
    unidade_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("ADMIN", "GERENTE"))
):
    unidade = db.query(Unidade).filter(Unidade.id == unidade_id).first()
    if not unidade:
        raise HTTPException(status_code=404, detail={
            "error": "UNIDADE_NAO_ENCONTRADA",
            "message": f"Unidade {unidade_id} não encontrada.",
            "details": [],
            "timestamp": datetime.utcnow().isoformat(),
            "path": f"/estoque/{unidade_id}"
        })
    return db.query(Estoque).filter(Estoque.unidade_id == unidade_id).all()

@router.post("/entrada", response_model=EstoqueResponse, status_code=201)
def entrada_estoque(
    body: EntradaEstoque,
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("ADMIN", "GERENTE"))
):
    if body.quantidade <= 0:
        raise HTTPException(status_code=422, detail={
            "error": "QUANTIDADE_INVALIDA",
            "message": "A quantidade deve ser maior que zero.",
            "details": [{"field": "quantidade", "issue": "deve ser > 0"}],
            "timestamp": datetime.utcnow().isoformat(),
            "path": "/estoque/entrada"
        })

    unidade = db.query(Unidade).filter(Unidade.id == body.unidade_id).first()
    if not unidade:
        raise HTTPException(status_code=404, detail={
            "error": "UNIDADE_NAO_ENCONTRADA",
            "message": f"Unidade {body.unidade_id} não encontrada.",
            "details": [],
            "timestamp": datetime.utcnow().isoformat(),
            "path": "/estoque/entrada"
        })

    produto = db.query(Produto).filter(Produto.id == body.produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail={
            "error": "PRODUTO_NAO_ENCONTRADO",
            "message": f"Produto {body.produto_id} não encontrado.",
            "details": [],
            "timestamp": datetime.utcnow().isoformat(),
            "path": "/estoque/entrada"
        })

    # Busca estoque existente ou cria novo
    estoque = db.query(Estoque).filter(
        Estoque.unidade_id == body.unidade_id,
        Estoque.produto_id == body.produto_id
    ).first()

    if not estoque:
        estoque = Estoque(
            unidade_id=body.unidade_id,
            produto_id=body.produto_id,
            quantidade=0
        )
        db.add(estoque)
        db.flush()

    estoque.quantidade += body.quantidade

    movimentacao = MovimentacaoEstoque(
        estoque_id=estoque.id,
        tipo="ENTRADA",
        quantidade=body.quantidade,
        motivo=body.motivo
    )
    db.add(movimentacao)
    registrar_auditoria(db, acao="ENTRADA_ESTOQUE", entidade="estoque", usuario_id=usuario.id, entidade_id=estoque.id, detalhes={"produto_id": body.produto_id, "unidade_id": body.unidade_id, "quantidade": body.quantidade})
    db.commit()
    db.refresh(estoque)
    return estoque

@router.get("/{unidade_id}/movimentacoes", response_model=list[MovimentacaoResponse])
def listar_movimentacoes(
    unidade_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("ADMIN", "GERENTE"))
):
    estoques = db.query(Estoque).filter(Estoque.unidade_id == unidade_id).all()
    if not estoques:
        return []
    estoque_ids = [e.id for e in estoques]
    return db.query(MovimentacaoEstoque).filter(
        MovimentacaoEstoque.estoque_id.in_(estoque_ids)
    ).order_by(MovimentacaoEstoque.created_at.desc()).all()
