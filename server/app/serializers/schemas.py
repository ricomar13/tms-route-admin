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
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    second_last_name: Optional[str] = None    
    role: Optional[str] = None
    
    class Config:
        from_attributes = True

class UpdateUser(SQLModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    second_last_name: Optional[str] = None
    role: Optional[str] = None