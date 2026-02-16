from sqlmodel import Session, select
from typing import Optional
from app.serializers.schemas import CreateUser, UpdateUser
from app.models.models import User
from config.security import get_password_hash

def create_user(session: Session, create_user: CreateUser):
    # Hash de la contraseña antes de guardar
    hashed_password = get_password_hash(create_user.password)
    user_data = create_user.model_dump(exclude={"password"})
    
    user = User(**user_data, hashed_password=hashed_password)
    
    session.add(user)
    session.commit()    
    session.refresh(user)
    
    # Generar código de empleado automático
    user.user_code = f"USER{user.id:05d}"
    session.commit()
    session.refresh(user)
    return user 

def get_users(session: Session, offset: int = 0, limit: int = 100):
    statement = select(User).offset(offset).limit(limit)
    return session.exec(statement).all()

def get_user_by_username(session: Session, username: str) -> Optional[User]:
    statement = select(User).where(User.username == username)
    return session.exec(statement).first()

def get_user_by_id(session: Session, user_id: int):
    return session.get(User, user_id)

def update_user(session: Session, user_id: int, user_update: UpdateUser):
    db_user = session.get(User, user_id)
    if not db_user:
        return None
        
    update_data = user_update.model_dump(exclude_unset=True)
    
    # Si el usuario mandó una contraseña nueva en el formulario
    if "password" in update_data:
        if update_data["password"]: 
            # SE ENCRIPTA AQUÍ ANTES DE GUARDAR
            db_user.hashed_password = get_password_hash(update_data["password"])
        # Quitamos 'password' del diccionario para que no intente 
        # guardarlo como una columna normal
        del update_data["password"] 
    
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def delete_user(session: Session, user_id: int) -> bool:
    user = session.get(User, user_id)
    if not user:
        return False
    session.delete(user)    
    session.commit()
    return True