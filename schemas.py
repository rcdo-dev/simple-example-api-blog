from pydantic import BaseModel, Field

# --- Modelos de Usuário ---


# 1. UserCreate: Schema para a criação de um usuário (Entrada POST)
# Omitimos o 'id' e 'posts' (que são gerados/relacionados pelo DB)
class UserCreate(BaseModel):
    username: str
    email: str
    password: str = Field(
        ..., max_length=72, description="Senha do usuário (máximo 72 bytes)."
    )


# 2. UserPublic: Schema para a resposta do usuário (Saída GET/POST)
# Incluímos o 'id' (gerado pelo DB), mas omitimos a 'password'
class UserPublic(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True  # Necessário para ler dados do ORM (DB)


# --- Modelos de Post ---


# 3. PostCreate: Schema para a criação de um post (Entrada POST)P
# Omitimos o 'id' (gerado) e o 'author' (o relacionamento), mas incluímos o author_id
class PostCreate(BaseModel):
    title: str
    content: str
    published: bool = True
    author_id: int  # Chave Estrangeira que o cliente deve enviar


# 4. PostPublic: Schema para a resposta do post (Saída GET/POST)
# Incluímos o 'id' e o 'author' (objeto aninhado)
class PostPublic(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    author: UserPublic  # O objeto Author aninhado (usando o schema de saída de usuário)

    class Config:
        from_attributes = True
