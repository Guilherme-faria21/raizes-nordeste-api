from sqlalchemy.orm import Session
from app.infrastructure.models import PontosFildelidade
from datetime import datetime


def _get_ou_criar_registro(db: Session, usuario_id: int) -> PontosFildelidade:
    """Busca o registro de pontos do usuário ou cria um novo zerado."""
    registro = db.query(PontosFildelidade).filter(
        PontosFildelidade.usuario_id == usuario_id
    ).first()

    if not registro:
        registro = PontosFildelidade(
            usuario_id=usuario_id,
            pontos_acumulados=0,
            pontos_resgatados=0,
            pontos_disponiveis=0,
        )
        db.add(registro)
        db.flush()  # garante que o objeto tem id sem commitar ainda

    return registro


def acumular_pontos(db: Session, usuario_id: int, total_pedido: float) -> dict:
    """
    Acumula pontos após pagamento aprovado.
    Regra: 1 ponto por R$1,00 gasto (arredondado para baixo).
    """
    pontos_ganhos = int(total_pedido)  # floor: R$31,90 → 31 pontos

    registro = _get_ou_criar_registro(db, usuario_id)
    registro.pontos_acumulados += pontos_ganhos
    registro.pontos_disponiveis += pontos_ganhos

    return {
        "pontos_ganhos": pontos_ganhos,
        "pontos_disponiveis": registro.pontos_disponiveis,
        "pontos_acumulados": registro.pontos_acumulados,
    }


def resgatar_pontos(db: Session, usuario_id: int, pontos: int) -> dict:
    """
    Resgata pontos do saldo disponível.
    Retorna erro se saldo insuficiente.
    """
    registro = _get_ou_criar_registro(db, usuario_id)

    if registro.pontos_disponiveis < pontos:
        return {
            "sucesso": False,
            "motivo": "SALDO_INSUFICIENTE",
            "pontos_disponiveis": registro.pontos_disponiveis,
        }

    registro.pontos_resgatados += pontos
    registro.pontos_disponiveis -= pontos

    return {
        "sucesso": True,
        "pontos_resgatados": pontos,
        "pontos_disponiveis": registro.pontos_disponiveis,
    }


def consultar_saldo(db: Session, usuario_id: int) -> dict:
    """Retorna o saldo atual de pontos do usuário."""
    registro = _get_ou_criar_registro(db, usuario_id)
    return {
        "usuario_id": usuario_id,
        "pontos_acumulados": registro.pontos_acumulados,
        "pontos_resgatados": registro.pontos_resgatados,
        "pontos_disponiveis": registro.pontos_disponiveis,
    }
