from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from core.database import get_session
from models import Post, User
from schemas import PostCreate, PostPublic
from utilities.dependencies import check_max_limit, get_current_active_user

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post(
    "/",
    response_model=PostPublic,
    status_code=status.HTTP_201_CREATED,
    responses={
        403: {"description": "Não autorizado a criar o post."},
        404: {"description": "Recurso não encontrado."},
    },
)
def create_post(post: PostCreate, db: Session = Depends(get_session)):
    author_exists = db.get(User, post.author_id)
    if not author_exists:
        raise HTTPException(
            status_code=404, detail=f"Autor com ID {post.author_id} não encontrado."
        )

    db_post = Post.model_validate(post)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.get("/", response_model=List[PostPublic])  # Agora retornando do DB de verdade
def list_posts(
    limit: int = Depends(check_max_limit),
    published: bool = True,
    search: Optional[str] = None,
    db: Session = Depends(get_session),
):
    # Criando a query base
    statement = select(Post)

    # Exemplo de como aplicar filtros reais se quiser:
    # if published: statement = statement.where(Post.published == True)

    results = db.exec(statement.limit(limit)).all()
    return results


@router.get("/{post_id}", response_model=PostPublic)
def read_post(post_id: int, db: Session = Depends(get_session)):
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=404, detail=f"Post com ID {post_id} não encontrado."
        )
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
):
    """
    Deleta um post se ele pertencer ao usuário logado.
    """
    post_db = db.get(Post, post_id)

    if not post_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post não encontrado"
        )

    if post_db.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
            detail="Não autorizado a deletar este post.",
        )

    db.delete(post_db)
    db.commit()
    return None
