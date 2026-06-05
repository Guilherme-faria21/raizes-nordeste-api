import json
from sqlalchemy.orm import Session
from app.infrastructure.models import LogAuditoria


def registrar(
    db: Session,
    acao: str,
    entidade: str,
    usuario_id: int = None,
    entidade_id: int = None,
    detalhes: dict = None,
) -> LogAuditoria:
    """
    Grava um registro de auditoria no banco.

    Parâmetros:
        acao        — ex: 'CRIAR_PEDIDO', 'LOGIN', 'RESGATAR_PONTOS'
        entidade    — ex: 'pedido', 'usuario', 'estoque'
        usuario_id  — quem executou a ação (None se não autenticado)
        entidade_id — ID do registro afetado (None se não aplicável)
        detalhes    — dict com informações extras (serializado como JSON)
    """
    log = LogAuditoria(
        usuario_id=usuario_id,
        acao=acao,
        entidade=entidade,
        entidade_id=entidade_id,
        detalhes=json.dumps(detalhes, ensure_ascii=False) if detalhes else None,
    )
    db.add(log)
    # Não fazemos commit aqui — quem chama decide quando commitar
    return log
