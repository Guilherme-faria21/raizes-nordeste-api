from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.infrastructure.database import get_db
from app.infrastructure.models import Unidade
from app.api.deps import get_usuario_atual, require_perfil

router = APIRouter(prefix="/unidades", tags=["Unidades"])

class UnidadeCreate(BaseModel):
    nome: str
    cidade: str
    estado: str
    endereco: Optional[str] = None
    ativa: Optional[bool] = True

class UnidadeResponse(BaseModel):
    id: int
    nome: str
    cidade: str
    estado: str
    endereco: Optional[str]
    ativa: bool

    class Config:
        from_attributes = True

@router.get("/", response_model=list[UnidadeResponse])
def listar_unidades(
    db: Session = Depends(get_db)
):
    return db.query(Unidade).filter(Unidade.ativa == True).all()

@router.get("/{unidade_id}", response_model=UnidadeResponse)
def buscar_unidade(
    unidade_id: int,
    db: Session = Depends(get_db)
):
    unidade = db.query(Unidade).filter(Unidade.id == unidade_id, Unidade.ativa == True).first()
    if not unidade:
        raise HTTPException(status_code=404, detail={
            "error": "UNIDADE_NAO_ENCONTRADA",
            "message": f"Unidade {unidade_id} não encontrada.",
            "details": [],
            "timestamp": datetime.utcnow().isoformat(),
            "path": f"/unidades/{unidade_id}"
        })
    return unidade

@router.post("/", response_model=UnidadeResponse, status_code=201)
def criar_unidade(
    dados: UnidadeCreate,
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("ADMIN", "GERENTE"))
):
    unidade = Unidade(**dados.model_dump())
    db.add(unidade)
    db.commit()
    db.refresh(unidade)
    return unidade

@router.put("/{unidade_id}", response_model=UnidadeResponse)
def atualizar_unidade(
    unidade_id: int,
    dados: UnidadeCreate,
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("ADMIN", "GERENTE"))
):
    unidade = db.query(Unidade).filter(Unidade.id == unidade_id, Unidade.ativa == True).first()
    if not unidade:
        raise HTTPException(status_code=404, detail={
            "error": "UNIDADE_NAO_ENCONTRADA",
            "message": f"Unidade {unidade_id} não encontrada.",
            "details": [],
            "timestamp": datetime.utcnow().isoformat(),
            "path": f"/unidades/{unidade_id}"
        })
    for campo, valor in dados.model_dump().items():
        setattr(unidade, campo, valor)
    db.commit()
    db.refresh(unidade)
    return unidade

@router.delete("/{unidade_id}", status_code=204)
def deletar_unidade(
    unidade_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("ADMIN"))
):
    unidade = db.query(Unidade).filter(Unidade.id == unidade_id).first()
    if not unidade:
        raise HTTPException(status_code=404, detail={
            "error": "UNIDADE_NAO_ENCONTRADA",
            "message": f"Unidade {unidade_id} não encontrada.",
            "details": [],
            "timestamp": datetime.utcnow().isoformat(),
            "path": f"/unidades/{unidade_id}"
        })
    unidade.ativa = False
    db.commit()
    return None
    db.commit()
