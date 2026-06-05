from datetime import datetime, timezone


def processar_pagamento(valor: float, metodo: str) -> dict:
    """
    Mock determinístico de pagamento.

    Métodos aprovados:
    - PIX
    - CARTAO_CREDITO
    - CARTAO_DEBITO
    - DINHEIRO
    - MOCK

    Métodos recusados:
    - RECUSADO
    - MOCK_RECUSADO
    - CARTAO_RECUSADO
    - CARTAO_CREDITO_RECUSADO
    """

    metodo_normalizado = (metodo or "MOCK").upper()

    metodos_recusados = {
        "RECUSADO",
        "MOCK_RECUSADO",
        "CARTAO_RECUSADO",
        "CARTAO_CREDITO_RECUSADO",
    }

    aprovado = metodo_normalizado not in metodos_recusados

    return {
        "aprovado": aprovado,
        "metodo": metodo_normalizado,
        "valor": valor,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "codigo_autorizacao": f"AUTH-MOCK-{metodo_normalizado}" if aprovado else None,
        "motivo_recusa": None if aprovado else "Transação recusada pelo mock de pagamento.",
    }
