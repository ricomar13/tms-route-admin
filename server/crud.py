from sqlmodel import Session, select
from schemas import CreateUser, UpdateUser
from models import User
from passlib.context import CryptContext
from security import get_password_hash
from typing import Optional

def create_user(session: Session, create_user: CreateUser):
    # Hash the password before storing it
    hashed_password = get_password_hash(create_user.password)

    # dicctionary without password
    user_data = create_user.model_dump(exclude={"password"})
    
    # user instance
    user = User(**user_data, hashed_password=hashed_password)
    
    session.add(user)
    session.commit()    
    session.refresh(user)
    
    user.user_code = f"USER{user.id:05d}"
    session.commit()
    session.refresh(user)
    return user 


def get_users(session: Session, offset: int = 0, limit: int = 100):
    statement = select(User).offset(offset).limit(limit)
    results = session.exec(statement)
    users = results.all()
    
    return users

def get_user_by_username(session: Session, username: str) -> Optional[User]:
    """Busca un usuario por su nombre de usuario."""
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()
    return user

def get_user_by_id(session: Session, user_id: int):
    user = session.get(User, user_id)
    return user

def update_user(session: Session, user_id: int, user_update: UpdateUser):
    user = session.get(User, user_id)
    if not user:
        return None
    #Update fields if they are provided
    user_data = user_update.model_dump(exclude_unset=True)
    
    # --- LÓGICA NUEVA PARA LA CONTRASEÑA ---
    # Si se envió una nueva contraseña en la petición...
    if "password" in user_data and user_data["password"]:
        # ...la hasheamos...
        hashed_password = get_password_hash(user_data["password"])
        user.hashed_password = hashed_password
        # ...y la eliminamos del diccionario para no intentar asignarla de nuevo.
        del user_data["password"]
    # ------------------------------------
    
    for key, value in user_data.items():
        setattr(user, key, value)
    
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return user

def delete_user(session: Session, user_id: int) ->bool:
    user = session.get(User, user_id)
    if not user:
        return False
    
    session.delete(user)    
    session.commit()
    
    return True