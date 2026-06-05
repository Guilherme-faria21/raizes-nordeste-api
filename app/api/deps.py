from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.infrastructure.security import decodificar_token
from app.infrastructure import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_usuario_atual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> models.Usuario:
    credenciais_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "error": "TOKEN_INVALIDO",
            "message": "Credenciais inválidas ou token expirado."
        },
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decodificar_token(token)
    if payload is None:
        raise credenciais_exception

    usuario_id: int = payload.get("sub")
    if usuario_id is None:
        raise credenciais_exception

    usuario = db.query(models.Usuario).filter(models.Usuario.id == int(usuario_id)).first()
    if usuario is None or not usuario.ativo:
        raise credenciais_exception

    return usuario

def require_perfil(*perfis: str):
    def verificar(usuario: models.Usuario = Depends(get_usuario_atual)):
        if usuario.perfil not in perfis:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "SEM_PERMISSAO",
                    "message": f"Acesso restrito. Perfis permitidos: {list(perfis)}"
                }
            )
        return usuario
    return verificar
