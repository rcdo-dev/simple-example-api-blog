from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from core.database import get_session
from ..models import User
from ..schemas import UserCreate, UserPublic
from core.security import get_password_hash
from ..utilities.dependencies import get_current_active_user # Para rotas protegidas

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# Rota protegida: GET /users/me
@router.get("/me", response_model=UserPublic)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Retorna o perfil do usuário logado."""
    return current_user

# Rota para criar usuário: POST /users/
@router.post("/", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_session)):
    # ... (Lógica de validação de 72 bytes e verificação de usuário existente)
    if len(user.password.encode('utf-8')) > 72:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A senha excede o limite máximo de 72 bytes. Por favor, use uma senha mais curta."
        )
    
    existig_user = db.exec(select(User).where(User.email == user.email)).first()
    if existig_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="E-mail já registrado")

    hashed_password = get_password_hash(user.password)

    db_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Rota para ler todos os usuários: GET /users/
@router.get("/", response_model=List[UserPublic])
def read_users(db: Session = Depends(get_session)):
    """Retorna a lista de todos os usuários."""
    statement = select(User)
    results = db.exec(statement).all()
    return results