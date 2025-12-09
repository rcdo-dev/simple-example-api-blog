from pydantic import BaseModel, Field

# --- Modelos de Usuário ---

# 1. UserCreate: Schema para a criação de um usuário (Entrada POST)
# Omitimos o 'id' e 'posts' (que são gerados/relacionados pelo DB)
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

# 2. UserPublic: Schema para a resposta do usuário (Saída GET/POST)
# Incluímos o 'id' (gerado pelo DB), mas omitimos a 'password'
class UserPublic(BaseModel):
    id: int
    username: str
    email: str
    class Config:
        from_attributes = True # Necessário para ler dados do ORM (DB)

# --- Modelos de Post ---

# 3. PostCreate: Schema para a criação de um post (Entrada POST)
# Omitimos o 'id' (gerado) e o 'author' (o relacionamento), mas incluímos o author_id
class PostCreate(BaseModel):
    title: str
    content: str
    published: bool = True
    author_id: int # Chave Estrangeira que o cliente deve enviar

# 4. PostPublic: Schema para a resposta do post (Saída GET/POST)
# Incluímos o 'id' e o 'author' (objeto aninhado)
class PostPublic(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    author: UserPublic # O objeto Author aninhado (usando o schema de saída de usuário)
    
    class Config:
        from_attributes = True

#------------------------------------------------------------------------------------------------------------

### Schema obsoleto - usando Pydantic puro.

# class Author(BaseModel):
#     name: str
#     bio: Optional[str] = None

# class PostBase(BaseModel):
#     title: str = Field(..., min_length=5, description="Título do post.")
#     content: str
#     published: bool = True

#     tags: List[str] = []

#     author: Author

#     class Config:
#         schema_extra = {
#             "example": {
#                 "title": "Aprenda a Aninhar Modelos",
#                 "content": "Modelos Pydantic dentro de outros modelos garantem dados estruturados.",
#                 "published": True,
#                 "tags": ["fastapi", "pydantic", "python"],
#                 "author":{
#                     "name": "Prof. FastAPI",
#                     "bio": "Especialista em APIs de alta performance."
#                 }
#             }
#         }

# class PostDisplay(BaseModel):
#     title: str
#     content: str
#     published: bool
#     id: int

#     class Config:
#         from_attributes = True