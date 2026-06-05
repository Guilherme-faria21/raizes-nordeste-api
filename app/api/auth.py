from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.infrastructure.database import get_db
from app.infrastructure.security import hash_senha, verificar_senha, criar_token
from app.application.auditoria_service import registrar as registrar_auditoria
from app.infrastructure import models

router = APIRouter(prefix="/auth", tags=["Auth"])

class RegistroRequest(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    perfil: Optional[str] = "CLIENTE"
    consentimento_lgpd: bool = False

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    perfil: str
    nome: str

@router.post("/registro", status_code=201)
def registrar(dados: RegistroRequest, db: Session = Depends(get_db)):
    if not dados.consentimento_lgpd:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "CONSENTIMENTO_OBRIGATORIO",
                "message": "O consentimento LGPD é obrigatório para cadastro."
            }
        )
    existente = db.query(models.Usuario).filter(models.Usuario.email == dados.email).first()
    if existente:
        raise HTTPException(
            status_code=409,
            detail={
                "error": "EMAIL_DUPLICADO",
                "message": "Já existe um usuário com esse e-mail."
            }
        )
    perfis_validos = [p.value for p in models.PerfilUsuario]
    if dados.perfil not in perfis_validos:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "PERFIL_INVALIDO",
                "message": f"Perfil inválido. Use um de: {perfis_validos}"
            }
        )
    usuario = models.Usuario(
        nome=dados.nome,
        email=dados.email,
        senha_hash=hash_senha(dados.senha),
        perfil=dados.perfil,
        consentimento_lgpd=dados.consentimento_lgpd
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return {"id": usuario.id, "nome": usuario.nome, "email": usuario.email, "perfil": usuario.perfil}

@router.post("/login", response_model=TokenResponse)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.email == form.username).first()
    if not usuario or not verificar_senha(form.password, usuario.senha_hash):
        raise HTTPException(
            status_code=401,
            detail={
                "error": "CREDENCIAIS_INVALIDAS",
                "message": "E-mail ou senha inválidos."
            }
        )
    token = criar_token({"sub": str(usuario.id), "perfil": usuario.perfil})
    registrar_auditoria(db, acao="LOGIN", entidade="usuario", usuario_id=usuario.id, entidade_id=usuario.id, detalhes={"perfil": usuario.perfil})
    db.commit()
    return {
        "access_token": token,
        "token_type": "bearer",
        "perfil": usuario.perfil,
        "nome": usuario.nome
    }
