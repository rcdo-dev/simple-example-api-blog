from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.database import create_db_and_tables
from routers import auth, posts, users


def on_start_up():
    print("Iniciando e criando o DB e as tabelas...")
    create_db_and_tables()


app = FastAPI(
    title="Api de Blog do Professor.",
    description="Uma API RESTFul completa para gerenciar posts de blog e usuários",
    version="1.0.0",
    on_startup=[on_start_up],
    openapi_tags=[
        {"name": "posts", "description": "Operações CRUD em posts de blog."},
        {"name": "users", "description": "Operações de usuário e autenticação."},
    ],
)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)


@app.get("/")
def home():
    """
    Rota raíz da API.
    """
    return {"message": "FastAPI Blog API"}
