import random
from datetime import datetime

def processar_pagamento(valor: float, metodo: str) -> dict:
    """
    Mock de pagamento.
    - PIX: 95% de aprovação
    - CARTAO_CREDITO: 85% de aprovação
    - CARTAO_DEBITO: 90% de aprovação
    - DINHEIRO: sempre aprovado
    """
    taxas_aprovacao = {
        "PIX": 0.95,
        "CARTAO_CREDITO": 0.85,
        "CARTAO_DEBITO": 0.90,
        "DINHEIRO": 1.0
    }

    taxa = taxas_aprovacao.get(metodo.upper(), 0.80)
    aprovado = random.random() < taxa

    return {
        "aprovado": aprovado,
        "metodo": metodo.upper(),
        "valor": valor,
        "timestamp": datetime.utcnow().isoformat(),
        "codigo_autorizacao": f"AUTH-{random.randint(100000, 999999)}" if aprovado else None,
        "motivo_recusa": None if aprovado else "Transação não autorizada pela operadora."
    }
