# main.py

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional
# from schemas import PostBase, PostDisplay
from sqlmodel import Session, select
from typing import List

from database import engine, create_db_and_tables, get_session
from dependencies import check_max_limit, ckeck_admin_permission
from models import User, Post
from schemas import UserCreate, UserPublic, PostCreate, PostPublic
from security import get_password_hash, verify_password

def on_start_up():
    print("Iniciando e criando o DB e as tabelas...")
    create_db_and_tables()


app = FastAPI(
    title="Api de Blog do Professor.",
    description="Uma API RESTFul completa para gerenciar posts de blog e usuários",
    version="1.0.0",
    on_startup=[on_start_up],
    openapi_tags=[
        {
            "name": "posts",
            "description": "Operações CRUD em posts de blog."
        },
        {
            "name": "users",
            "description": "Operações de usuário e autenticação."
        }
    ]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
@app.post("/auth/token", tags=["users"])
def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_session)
):
    """
    Recebe username (email) e password e verifica as credenciais.
    """

    user = db.exec(select(User).where(User.email == form_data.username)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas.",
            headers={"WWW-Authenticate":"Bearer"}
        )
    
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas.",
            headers={"WWW-Authenticate":"Bearer"}
        )
    return {"message": "Autenticação bem-sucedida!"}

@app.get("/")
def home():
    """
    Rota raíz da API.
    """
    return {"message": "FastAPI Blog API"}

# -----------------------------------------------------------

@app.post(
    "/posts", tags=["posts"],
    response_model=PostPublic,
    status_code=status.HTTP_201_CREATED,
    responses={
        403:{"description": "Não autorizado a criar o post."},
        404:{"description": "Recurso não encontrado."}
    }
)
def create_post(post: PostCreate, db: Session = Depends(get_session)):
    """
    Cria um novo post e o associa a um autor (author_id).
    """
    author_exists = db.get(User, post.author_id)
    if not author_exists:
        raise HTTPException(status_code=404, detail=f"Autor com ID {post.author_id} não encontrado.")

    db_post = Post.model_validate(post)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# -----------------------------------------------------------

@app.get("/posts", tags=["posts"])
def list_posts(limit: int = Depends(check_max_limit), published: bool = True, search: Optional[str] = None):
    """
    Retorna uma lista com todos os posts.
    """
    if search:
        print(f"Buscanso posts com o termo {search}")
        return {"message":f"Retornando posts com o termo '{search}' e limit {limit}."}

    if published:
        message = f"Retornando os últimos {limit} posts publicados."
    else:
        message = f"Retornando os últimos {limit} posts (publicados e rascunhos)."
    return {"message": message, "limit": limit, "published": published}

# -----------------------------------------------------------

@app.get("/posts/{post_id}", response_model=PostPublic, tags=["posts"])
def read_post(post_id: int, db: Session=Depends(get_session)):
    """
    Retorna um post específico, incluindo os detalhes do autor.
    """

    post = db.get(Post, post_id)

    if not post:
        raise HTTPException(
            status_code=404,
            detail=f"Post com ID {post_id} não encontrado."
        )
    
    return post

# -----------------------------------------------------------

@app.put("/posts/{post_id}", tags=["posts"])
def update_post(post_id: int, post: PostCreate):
    """
    Atualiza uma postagem através do ID e do conteúdo a ser atualizado.
    """
    return{
        "message":f"Post {post_id} atualizado com sucesso.",
        "new_data": post.model_dump()
    }

# -----------------------------------------------------------

@app.delete("/posts/{post_id}", tags=["posts"], status_code=204)
def delete_post(post_id: int, admin_user: dict = Depends(ckeck_admin_permission)):
    """
    Deleta um post específico pelo ID, requer permissão de adminstrador.
    """
    print(f"Usuário {admin_user['username']} autorizado a deletar post {post_id}")

    return {"message": f"Post com ID {post_id} deletado."}

# -----------------------------------------------------------

@app.post("/users", response_model=UserPublic, tags=["users"], status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_session)):
    """
    Cria o registro de um novo usuário.
    """

    # 1. Verificar se o usuário já existe
    existig_user = db.exec(select(User).where(User.email == user.email)).first()
    if existig_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="E-mail já registrado")

    # 2. HASH DA SENHA: Esta é a linha crucial de segurança
    hashed_password = get_password_hash(user.password)

    # 3. Cria um objeto do DB, usando a senha hasheada
    db_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password # Salva o hash, não a senha em texto puro
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users", response_model=List[UserPublic], tags=["users"])
def read_users(db: Session = Depends(get_session)):
    """
    Retorna a lista de todos os usuários.
    """
    statement = select(User)
    results = db.exec(statement).all()
    return results