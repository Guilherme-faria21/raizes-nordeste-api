from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from datetime import datetime

from app.infrastructure.database import get_db
from app.api.deps import get_usuario_atual, require_perfil
from app.application.auditoria_service import registrar as registrar_auditoria
from app.application.fidelidade_service import (
    consultar_saldo,
    resgatar_pontos,
)

router = APIRouter(prefix="/fidelidade", tags=["Fidelidade"])


def _erro(code: str, msg: str, status: int, path: str):
    raise HTTPException(
        status_code=status,
        detail={
            "error": code,
            "message": msg,
            "details": [],
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "path": path,
        },
    )


class ResgateRequest(BaseModel):
    pontos: int = Field(..., gt=0, description="Quantidade de pontos a resgatar")


# ─── GET /fidelidade/saldo ───────────────────────────────────────────────────
@router.get("/saldo", summary="Consultar saldo de pontos do usuário autenticado")
def get_saldo(
    db: Session = Depends(get_db),
    usuario=Depends(get_usuario_atual),
):
    """
    Qualquer usuário autenticado pode ver seu próprio saldo.
    ADMIN/GERENTE podem ver o saldo de qualquer usuário via /saldo/{usuario_id}.
    """
    return consultar_saldo(db, usuario.id)


# ─── GET /fidelidade/saldo/{usuario_id} ─────────────────────────────────────
@router.get(
    "/saldo/{usuario_id}",
    summary="Consultar saldo de pontos de um usuário específico (ADMIN/GERENTE)",
    dependencies=[Depends(require_perfil("ADMIN", "GERENTE"))],
)
def get_saldo_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_usuario_atual),
):
    saldo = consultar_saldo(db, usuario_id)
    return saldo


# ─── POST /fidelidade/resgatar ───────────────────────────────────────────────
@router.post("/resgatar", summary="Resgatar pontos do saldo disponível")
def post_resgatar(
    body: ResgateRequest,
    db: Session = Depends(get_db),
    usuario=Depends(get_usuario_atual),
):
    resultado = resgatar_pontos(db, usuario.id, body.pontos)

    if not resultado["sucesso"]:
        _erro(
            "SALDO_INSUFICIENTE",
            f"Saldo insuficiente. Disponível: {resultado['pontos_disponiveis']} pontos.",
            409,
            "/fidelidade/resgatar",
        )

    registrar_auditoria(db, acao="RESGATAR_PONTOS", entidade="fidelidade", usuario_id=usuario.id, detalhes={"pontos_resgatados": body.pontos, "saldo_apos": resultado["pontos_disponiveis"]})
    db.commit()
    return {
        "message": f"{body.pontos} pontos resgatados com sucesso.",
        "pontos_resgatados": resultado["pontos_resgatados"],
        "pontos_disponiveis": resultado["pontos_disponiveis"],
    }
