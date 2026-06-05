"""
seed.py — Popula o banco com dados iniciais para apresentação/testes.
Idempotente: pode ser executado multiplas vezes sem duplicar dados.
Uso: python seed.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.infrastructure.database import SessionLocal, engine
from app.infrastructure.models import Base
from app.infrastructure import models
from app.infrastructure.security import hash_senha

def seed():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    try:
        print("Iniciando seed do banco de dados...")

        # -----------------------------------------
        # USUARIOS
        # -----------------------------------------
        usuarios = [
            {"nome": "Admin",         "email": "admin@raizes.com",  "senha": "Admin@123",   "perfil": "ADMIN"},
            {"nome": "Gerente Recife","email": "gerente@raizes.com", "senha": "Gerente@123", "perfil": "GERENTE"},
            {"nome": "Maria Silva",   "email": "maria@email.com",    "senha": "Cliente@123", "perfil": "CLIENTE"},
            {"nome": "Joao Souza",    "email": "joao@email.com",     "senha": "Cliente@123", "perfil": "CLIENTE"},
        ]

        usuarios_ids = {}
        for u in usuarios:
            existente = db.query(models.Usuario).filter_by(email=u["email"]).first()
            if not existente:
                novo = models.Usuario(
                    nome=u["nome"],
                    email=u["email"],
                    senha_hash=hash_senha(u["senha"]),
                    perfil=u["perfil"],
                    consentimento_lgpd=True,
                    ativo=True,
                )
                db.add(novo)
                db.flush()
                usuarios_ids[u["email"]] = novo.id
                print(f"  [OK] Usuario criado: {u['email']} ({u['perfil']})")
            else:
                usuarios_ids[u["email"]] = existente.id
                print(f"  [--] Usuario ja existe: {u['email']}")

        db.commit()

        # -----------------------------------------
        # UNIDADES
        # -----------------------------------------
        unidades_data = [
            {"nome": "Raizes do Nordeste - Recife Centro",       "cidade": "Recife",    "estado": "PE", "endereco": "Rua do Bom Jesus, 200"},
            {"nome": "Raizes do Nordeste - Fortaleza Beira Mar", "cidade": "Fortaleza", "estado": "CE", "endereco": "Av. Beira Mar, 1500"},
            {"nome": "Raizes do Nordeste - Natal Cidade Alta",   "cidade": "Natal",     "estado": "RN", "endereco": "Rua Chile, 45"},
        ]

        unidades_ids = []
        for u in unidades_data:
            existente = db.query(models.Unidade).filter_by(nome=u["nome"]).first()
            if not existente:
                nova = models.Unidade(
                    nome=u["nome"],
                    cidade=u["cidade"],
                    estado=u["estado"],
                    endereco=u["endereco"],
                    ativa=True,
                )
                db.add(nova)
                db.flush()
                unidades_ids.append(nova.id)
                print(f"  [OK] Unidade criada: {u['nome']}")
            else:
                unidades_ids.append(existente.id)
                print(f"  [--] Unidade ja existe: {u['nome']}")

        db.commit()

        # -----------------------------------------
        # PRODUTOS
        # -----------------------------------------
        produtos_data = [
            {"nome": "Cuscuz com Manteiga",     "descricao": "Cuscuz de milho com manteiga de garrafa artesanal",          "preco": 8.50},
            {"nome": "Tapioca de Carne de Sol", "descricao": "Tapioca recheada com carne de sol desfiada e queijo coalho", "preco": 14.90},
            {"nome": "Baiao de Dois",           "descricao": "Arroz com feijao de corda, queijo coalho e linguica",        "preco": 22.00},
            {"nome": "Caldinho de Feijao",      "descricao": "Caldinho temperado com coentro e bacon",                     "preco": 9.00},
            {"nome": "Suco de Caja",            "descricao": "Suco natural de caja 400ml",                                 "preco": 7.00},
            {"nome": "Cartola",                 "descricao": "Banana frita com queijo coalho e canela",                    "preco": 11.50},
        ]

        produtos_ids = []
        for p in produtos_data:
            existente = db.query(models.Produto).filter_by(nome=p["nome"]).first()
            if not existente:
                novo = models.Produto(
                    nome=p["nome"],
                    descricao=p["descricao"],
                    preco=p["preco"],
                    ativo=True,
                )
                db.add(novo)
                db.flush()
                produtos_ids.append(novo.id)
                print(f"  [OK] Produto criado: {p['nome']} (R${p['preco']:.2f})")
            else:
                produtos_ids.append(existente.id)
                print(f"  [--] Produto ja existe: {p['nome']}")

        db.commit()

        # -----------------------------------------
        # ESTOQUE
        # -----------------------------------------
        criados = 0
        for unidade_id in unidades_ids:
            for produto_id in produtos_ids:
                existente = db.query(models.Estoque).filter_by(
                    unidade_id=unidade_id, produto_id=produto_id
                ).first()
                if not existente:
                    db.add(models.Estoque(
                        unidade_id=unidade_id,
                        produto_id=produto_id,
                        quantidade=50,
                    ))
                    criados += 1

        db.commit()
        if criados:
            print(f"  [OK] Estoque populado: {criados} registros (50 un. cada)")
        else:
            print(f"  [--] Estoque ja populado")

        # -----------------------------------------
        # RESUMO
        # -----------------------------------------
        print("\n" + "=" * 50)
        print("Seed concluido com sucesso!")
        print("=" * 50)
        print("\nCredenciais para teste:")
        print("  ADMIN   -> admin@raizes.com   / Admin@123")
        print("  GERENTE -> gerente@raizes.com / Gerente@123")
        print("  CLIENTE -> maria@email.com    / Cliente@123")
        print("  CLIENTE -> joao@email.com     / Cliente@123")
        print(f"\nUnidades: {len(unidades_ids)}  |  Produtos: {len(produtos_ids)}  |  Estoques: {len(unidades_ids) * len(produtos_ids)}")
        print("\nPara iniciar a API: uvicorn main:app --reload")
        print("=" * 50 + "\n")

    except Exception as e:
        db.rollback()
        print(f"\nERRO durante o seed: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed()
