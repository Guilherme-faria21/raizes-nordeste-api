from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.infrastructure.database import get_db
from app.infrastructure.models import LogAuditoria
from app.api.deps import get_usuario_atual, require_perfil

router = APIRouter(prefix="/auditoria", tags=["Auditoria"])


@router.get(
    "/",
    summary="Listar logs de auditoria (ADMIN)",
    dependencies=[Depends(require_perfil("ADMIN"))],
)
def listar_logs(
    acao: Optional[str] = Query(None, description="Filtrar por ação ex: LOGIN, CRIAR_PEDIDO"),
    entidade: Optional[str] = Query(None, description="Filtrar por entidade ex: pedido, usuario"),
    usuario_id: Optional[int] = Query(None, description="Filtrar por usuário"),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _=Depends(get_usuario_atual),
):
    query = db.query(LogAuditoria)

    if acao:
        query = query.filter(LogAuditoria.acao == acao.upper())
    if entidade:
        query = query.filter(LogAuditoria.entidade == entidade.lower())
    if usuario_id:
        query = query.filter(LogAuditoria.usuario_id == usuario_id)

    logs = query.order_by(LogAuditoria.created_at.desc()).limit(limit).all()

    return [
        {
            "id": log.id,
            "usuario_id": log.usuario_id,
            "acao": log.acao,
            "entidade": log.entidade,
            "entidade_id": log.entidade_id,
            "detalhes": log.detalhes,
            "created_at": log.created_at,
        }
        for log in logs
    ]
