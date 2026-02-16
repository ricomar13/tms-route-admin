from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session
from typing import Annotated, List
from fastapi.security import OAuth2PasswordRequestForm
from app.services import crud
from app.serializers.schemas import CreateUser, ReadUser, UpdateUser
from app.models.models import User 
from config.database import get_session
from config import security

router = APIRouter(prefix="/users", tags=["users"])

SessionDep = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(security.get_current_user)]

# --- ENDPOINT DE LOGIN (ESTE ES EL QUE FALTABA EN TUS DOCS) ---
@router.post("/token")
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep
):
    """
    Autentica un usuario y devuelve un token JWT.
    """
    user = crud.get_user_by_username(session, username=form_data.username)
    
    # Verificamos si existe el usuario y si la contraseña coincide con el hash
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = security.create_access_token(
        data={"sub": user.username, "role": user.role} 
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

# --- GESTIÓN DE PERFIL ---

@router.get("/me", response_model=ReadUser)
def read_me(current_user: CurrentUser):
    return current_user

@router.patch("/me", response_model=ReadUser)
def update_me(
    user_update: UpdateUser, 
    current_user: CurrentUser, 
    session: SessionDep
):
    # Evitar duplicados si el usuario intenta cambiar su username
    if user_update.username and user_update.username != current_user.username:
        if crud.get_user_by_username(session, user_update.username):
            raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")

    updated_user = crud.update_user(
        session=session, 
        user_id=current_user.id, 
        user_update=user_update
    )
    
    if not updated_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return updated_user

# --- CRUD GENERAL ---

@router.post("/", response_model=ReadUser)
async def create(user: CreateUser, session: SessionDep):
    db_user = crud.get_user_by_username(session, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    return crud.create_user(session, user)

@router.get("/", response_model=List[ReadUser])
def read_all(session: SessionDep, offset: int = 0, limit: int = 100):
    return crud.get_users(session, offset=offset, limit=limit)

@router.delete("/{user_id}")
def delete(session: SessionDep, user_id: int):
    if not crud.delete_user(session, user_id):
        raise HTTPException(status_code=404, detail="No encontrado")
    return {"ok": True}