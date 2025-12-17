from fastapi import Depends, HTTPException
from sqlmodel import Session, select

from core.database import get_session
from core.security import get_current_user_email
from models import User


def check_max_limit(limit: int = 10):
    if limit > 100:
        raise HTTPException(
            status_code=400, detail="O limite máximo permitido para posts é 100."
        )
    return limit


def get_current_user(user_id: int = 1):
    return {"user_id": user_id, "username": "admin_simulado"}


def ckeck_admin_permission(current_user: dict = Depends(get_current_user)):
    if current_user["user_id"] != 1:
        raise HTTPException(
            status_code=403,
            detail="Acesso negado: Requer privilegios de administrador.",
        )
    return current_user


def get_current_active_user(
    current_user_email: str = Depends(get_current_user_email),
    db: Session = Depends(get_session),
) -> User:
    """
    Dependência que verifica o token, busca o usuário no DB e garante que ele existe.
    Retorna o objeto User completo.
    """
    # Buscamos o usuário no DB pelo email que veio do token
    user = db.exec(select(User).where(User.email == current_user_email)).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    # Poderíamos checar aqui se o usuário está ativo, se tivéssemos o campo 'is_active'
    return user
