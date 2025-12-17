from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True)
    password: str

    # 1. Relacionamento: Um usuário pode ter muitos posts (lazy loading)
    posts: List["Post"] = Relationship(back_populates="author")


class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    published: bool = True

    # 2. Foreign Key: Conecta o post ao autor (User)
    author_id: int = Field(foreign_key="user.id")

    # 3. Relacionamento: Um post pertence a um autor (eager loading)
    author: User = Relationship(back_populates="posts")
