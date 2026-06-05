import hashlib
import base64
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY", "chave-insegura-troque-no-env")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
TOKEN_EXPIRE = int(os.getenv("TOKEN_EXPIRE", "60"))

def _preparar_senha(senha: str) -> str:
    digest = hashlib.sha256(senha.encode()).digest()
    return base64.b64encode(digest).decode()

def hash_senha(senha: str) -> str:
    return pwd_context.hash(_preparar_senha(senha))

def verificar_senha(senha: str, hash: str) -> bool:
    return pwd_context.verify(_preparar_senha(senha), hash)

def criar_token(dados: dict) -> str:
    payload = dados.copy()
    expira = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE)
    payload.update({"exp": expira})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decodificar_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
