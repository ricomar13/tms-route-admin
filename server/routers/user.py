import crud
from fastapi import APIRouter, Depends, HTTPException, Query
from schemas import CreateUser, ReadUser, UpdateUser
from sqlmodel import Session
from database import get_session
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordRequestForm
import security
from models import User 
from security import oauth2_scheme

router = APIRouter(prefix="/users", tags=["users"])
SessionDep = Annotated[(Session, Depends(get_session))]
CurrentUser = Annotated[User, Depends(security.get_current_user)]


# Login y obtención de token
@router.post("/token")
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep
):
    """
    Autentica un usuario y devuelve un token de acceso JWT.
    """
    # 1. Busca al usuario en la base de datos por su username.
    user = crud.get_user_by_username(session, username=form_data.username)
    
    # 2. Si el usuario no existe O la contraseña es incorrecta, devuelve un error.
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El nombre de usuario o la contraseña son incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # 3. Si todo es correcto, crea el token JWT.
    #    Puedes incluir datos adicionales en el token, como el rol.
    access_token = security.create_access_token(
        data={"sub": user.username, "role": user.role} 
    )
    
    # 4. Devuelve el token. El frontend lo guardará para futuras peticiones.
    return {"access_token": access_token, "token_type": "bearer"}


# --- NUEVO ENDPOINT PARA ACTUALIZAR EL PERFIL ---
@router.patch("/me", response_model=ReadUser)
def update_me(
    user_update: UpdateUser, 
    current_user: CurrentUser, 
    session: SessionDep
):
    """
    Actualiza los datos del usuario actualmente autenticado.
    """
    # Reutilizamos la función de update del CRUD, pero nos aseguramos
    # de pasarle el ID del usuario que está logueado (current_user.id).
    updated_user = crud.update_user(
        session=session, 
        user_id=current_user.id, 
        user_update=user_update
    )
    if not updated_user:
        # Esto no debería pasar si el token es válido, pero es una buena práctica
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return updated_user

@router.get("/me", response_model=ReadUser)
def read_me(current_user: CurrentUser):
    """
    Obtiene los datos del usuario actualmente autenticado.
    """
    # La dependencia 'CurrentUser' ya hizo todo el trabajo de validar
    # el token y obtener el usuario de la base de datos.
    # Simplemente devolvemos el usuario que nos ha proporcionado.
    return current_user

@router.post("/", response_model=ReadUser)
async def create(user: CreateUser, session: SessionDep):
    db_user = crud.get_user_by_username(session, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está registrado")
    return crud.create_user(session, user)

@router.get("/", response_model=list[ReadUser])
#limite de query a 100 para evitar sobrecarga
def read_all(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100, ge=1)] = 100):
    return crud.get_users(session, offset=offset, limit=limit)

@router.get("/{user_id}", response_model=ReadUser)
def read(session: SessionDep, user_id: int) -> ReadUser:
    user = crud.get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return user

@router.put("/{user_id}", response_model=ReadUser)
def update(session: SessionDep, user_id: int, user_update: UpdateUser):
    updated = crud.update_user(session, user_id, user_update)
    if not updated:
        raise HTTPException(status_code=404, detail="No se puede modificar - Usuario no encontrado")
    
    return updated


@router.delete("/{user_id}")
def delete(session: SessionDep, user_id: int):
    deleted = crud.delete_user(session, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="No se puede eliminar - Usuario no encontrado")
    
    return {"ok": True}

