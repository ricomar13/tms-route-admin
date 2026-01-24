from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import EmailStr

class CreateUser(SQLModel):
    first_name: str  # Campo obligatorio
    middle_name: Optional[str] = None # Campo opcional
    last_name: str   # Campo obligatorio
    second_last_name: Optional[str] = None # Campo opcional
    email: EmailStr = Field(unique=True, index=True)
    password: str
    username: str = Field(unique=True, index=True)
    role: str = "default"  # Valor por defecto
    
class ReadUser(SQLModel):
    id: int
    user_code: Optional[str] = None 
    username: str
    email: EmailStr = Field(unique=True, index=True)
    full_name: str
    role: Optional[str] = None
    
class UpdateUser(SQLModel):
    username: Optional[str] 
    email: Optional[EmailStr] = Field(unique=True, index=True)
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    second_last_name: Optional[str]  
    role: Optional[str]
    password: Optional[str] = None