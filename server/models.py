from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import EmailStr

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # Columnas en la base de datos
    user_code: Optional[str] = Field(default=None, unique=True, index=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str 
    first_name: str
    middle_name: Optional[str] = Field(default=None)
    last_name: str
    second_last_name: Optional[str] = Field(default=None)
    email: EmailStr = Field(unique=True, index=True)
    role: Optional[str] = Field(default=None, index=True)

    #obtener el nombre completo.
    @property
    def full_name(self) -> str:
        parts = [self.first_name, self.middle_name, self.last_name, self.second_last_name]
        return " ".join(part for part in parts if part)