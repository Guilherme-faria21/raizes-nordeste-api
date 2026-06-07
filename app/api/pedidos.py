from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import json

from app.infrastructure.database import get_db
from app.infrastructure.models import (
    Pedido, ItemPedido, Pagamento, Estoque, MovimentacaoEstoque,
    Produto, Unidade, StatusPedido, StatusPagamento, CanalPedido
)
from app.api.deps import get_usuario_atual, require_perfil
from app.application.pagamento_service import processar_pagamento
from app.application.fidelidade_service import acumular_pontos
from app.application.auditoria_service import registrar as registrar_auditoria

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

# --- Schemas ---

class ItemPedidoCreate(BaseModel):
    produto_id: int
    quantidade: int

class PedidoCreate(BaseModel):
    unidade_id: int
    canal_pedido: CanalPedido
    forma_pagamento: str
    itens: list[ItemPedidoCreate]

class ItemPedidoResponse(BaseModel):
    id: int
    produto_id: int
    quantidade: int
    preco_unitario: float

    class Config:
        from_attributes = True

class PagamentoResponse(BaseModel):
    id: int
    status: str
    metodo: str
    valor: float
    resposta_gateway: Optional[str]

    class Config:
        from_attributes = True

class PedidoResponse(BaseModel):
    id: int
    unidade_id: int
    canal_pedido: str
    status: str
    total: float
    forma_pagamento: str
    created_at: datetime
    itens: list[ItemPedidoResponse]
    pagamento: Optional[PagamentoResponse]

    class Config:
        from_attributes = True

class AtualizarStatusRequest(BaseModel):
    novo_status: str

# --- Transições de status válidas (fluxo de cozinha) ---
TRANSICOES_VALIDAS = {
    "EM_PREPARO": ["PRONTO", "CANCELADO"],
    "PRONTO":     ["ENTREGUE"],
}

# --- Endpoints ---

@router.post("/", response_model=PedidoResponse, status_code=201)
def criar_pedido(
    body: PedidoCreate,
    db: Session = Depends(get_db),
    usuario=Depends(get_usuario_atual)
):
    # Valida unidade
    unidade = db.query(Unidade).filter(Unidade.id == body.unidade_id).first()
    if not unidade:
        raise HTTPException(status_code=404, detail={
            "error": "UNIDADE_NAO_ENCONTRADA",
            "message": f"Unidade {body.unidade_id} não encontrada.",
            "details": [],
            "timestamp": datetime.utcnow().isoformat(),
            "path": "/pedidos"
        })

    # Valida itens e estoque
    if not body.itens:
        raise HTTPException(status_code=422, detail={
            "error": "PEDIDO_SEM_ITENS",
            "message": "O pedido deve ter pelo menos um item.",
            "details": [],
            "timestamp": datetime.utcnow().isoformat(),
            "path": "/pedidos"
        })

    itens_validados = []
    erros_estoque = []

    for item in body.itens:
        produto = db.query(Produto).filter(
            Produto.id == item.produto_id,
            Produto.ativo == True
        ).first()
        if not produto:
            raise HTTPException(status_code=404, detail={
                "error": "PRODUTO_NAO_ENCONTRADO",
                "message": f"Produto {item.produto_id} não encontrado ou inativo.",
                "details": [],
                "timestamp": datetime.utcnow().isoformat(),
                "path": "/pedidos"
            })

        estoque = db.query(Estoque).filter(
            Estoque.unidade_id == body.unidade_id,
            Estoque.produto_id == item.produto_id
        ).first()

        if not estoque or estoque.quantidade < item.quantidade:
            disponivel = estoque.quantidade if estoque else 0
            erros_estoque.append({
                "field": f"itens[produto_id={item.produto_id}].quantidade",
                "issue": f"Disponível: {disponivel}"
            })
        else:
            itens_validados.append((item, produto, estoque))

    if erros_estoque:
        raise HTTPException(status_code=409, detail={
            "error": "ESTOQUE_INSUFICIENTE",
            "message": "Não há quantidade suficiente para um ou mais itens.",
            "details": erros_estoque,
            "timestamp": datetime.utcnow().isoformat(),
            "path": "/pedidos"
        })

    # Calcula total
    total = sum(produto.preco * item.quantidade for item, produto, _ in itens_validados)

    # Cria pedido
    pedido = Pedido(
        cliente_id=usuario.id,
        unidade_id=body.unidade_id,
        canal_pedido=body.canal_pedido.value,
        status=StatusPedido.AGUARDANDO_PAGAMENTO,
        total=total,
        forma_pagamento=body.forma_pagamento.upper()
    )
    db.add(pedido)
    db.flush()

    # Cria itens
    for item, produto, estoque in itens_validados:
        item_pedido = ItemPedido(
            pedido_id=pedido.id,
            produto_id=item.produto_id,
            quantidade=item.quantidade,
            preco_unitario=produto.preco
        )
        db.add(item_pedido)

    # Processa pagamento mock
    resultado_pagamento = processar_pagamento(total, body.forma_pagamento)

    status_pagamento = StatusPagamento.APROVADO if resultado_pagamento["aprovado"] else StatusPagamento.RECUSADO

    pagamento = Pagamento(
        pedido_id=pedido.id,
        status=status_pagamento,
        metodo=body.forma_pagamento.upper(),
        valor=total,
        resposta_gateway=json.dumps(resultado_pagamento)
    )
    db.add(pagamento)

    # Atualiza status do pedido e baixa estoque
    if resultado_pagamento["aprovado"]:
        pedido.status = StatusPedido.EM_PREPARO
        for item, produto, estoque in itens_validados:
            estoque.quantidade -= item.quantidade
            movimentacao = MovimentacaoEstoque(
                estoque_id=estoque.id,
                tipo="SAIDA",
                quantidade=item.quantidade,
                motivo=f"Pedido #{pedido.id}"
            )
            db.add(movimentacao)
        acumular_pontos(db, pedido.cliente_id, pedido.total)
        registrar_auditoria(db, acao="CRIAR_PEDIDO", entidade="pedido", usuario_id=pedido.cliente_id, entidade_id=pedido.id, detalhes={"total": pedido.total, "canal": pedido.canal_pedido, "status": "APROVADO"})
    else:
        pedido.status = StatusPedido.PAGAMENTO_RECUSADO
        registrar_auditoria(db, acao="PAGAMENTO_RECUSADO", entidade="pedido", usuario_id=pedido.cliente_id, entidade_id=pedido.id, detalhes={"total": pedido.total, "canal": pedido.canal_pedido})

    db.commit()
    db.refresh(pedido)
    return pedido


@router.get("/", response_model=list[PedidoResponse])
def listar_pedidos(
    canal_pedido: Optional[str] = Query(None, description="Filtrar por canal: APP, TOTEM, BALCAO, PICKUP, WEB"),
    db: Session = Depends(get_db),
    usuario=Depends(get_usuario_atual)
):
    # Cliente vê só os próprios pedidos, ADMIN/GERENTE veem todos
    if usuario.perfil in ["ADMIN", "GERENTE"]:
        query = db.query(Pedido)
    else:
        query = db.query(Pedido).filter(Pedido.cliente_id == usuario.id)

    if canal_pedido:
        query = query.filter(Pedido.canal_pedido == canal_pedido.upper())

    return query.order_by(Pedido.created_at.desc()).all()


@router.get("/{pedido_id}", response_model=PedidoResponse)
def buscar_pedido(
    pedido_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_usuario_atual)
):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail={
            "error": "PEDIDO_NAO_ENCONTRADO",
            "message": f"Pedido {pedido_id} não encontrado.",
            "details": [],
            "timestamp": datetime.utcnow().isoformat(),
            "path": f"/pedidos/{pedido_id}"
        })
    # Cliente só vê o próprio pedido
    if usuario.perfil == "CLIENTE" and pedido.cliente_id != usuario.id:
        raise HTTPException(status_code=403, detail={
            "error": "ACESSO_NEGADO",
            "message": "Você não tem permissão para acessar este pedido.",
            "details": [],
            "timestamp": datetime.utcnow().isoformat(),
            "path": f"/pedidos/{pedido_id}"
        })
    return pedido


@router.patch("/{pedido_id}/status", summary="Atualizar status do pedido (cozinha)")
def atualizar_status_pedido(
    pedido_id: int,
    body: AtualizarStatusRequest,
    db: Session = Depends(get_db),
    usuario_atual=Depends(require_perfil("ADMIN", "GERENTE")),
):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()

    if not pedido:
        raise HTTPException(status_code=404, detail={
            "error": "PEDIDO_NAO_ENCONTRADO",
            "message": f"Pedido {pedido_id} não encontrado.",
            "details": [],
            "timestamp": datetime.utcnow().isoformat(),
            "path": f"/pedidos/{pedido_id}/status"
        })

    status_atual = pedido.status
    novo_status = body.novo_status.upper()

    permitidos = TRANSICOES_VALIDAS.get(status_atual, [])
    if novo_status not in permitidos:
        raise HTTPException(status_code=422, detail={
            "error": "TRANSICAO_INVALIDA",
            "message": (
                f"Transição '{status_atual}' → '{novo_status}' não é permitida. "
                f"Transições válidas a partir de '{status_atual}': {permitidos}"
            ),
            "details": [],
            "timestamp": datetime.utcnow().isoformat(),
            "path": f"/pedidos/{pedido_id}/status"
        })

    pedido.status = novo_status
    db.commit()
    db.refresh(pedido)

    registrar_auditoria(
        db,
        acao="ATUALIZAR_STATUS_PEDIDO",
        entidade="pedido",
        usuario_id=usuario_atual.id,
        entidade_id=pedido.id,
        detalhes={"status_anterior": status_atual, "status_novo": novo_status}
    )

    return {
        "pedido_id": pedido.id,
        "status_anterior": status_atual,
        "status_atual": pedido.status,
    }
