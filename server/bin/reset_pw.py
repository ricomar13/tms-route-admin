import sys
import os
from sqlmodel import Session, select

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# IMPORTS ACTUALIZADOS
from config.database import engine
from app.models.models import User
from config.security import get_password_hash

def reset_admin_password():
    with Session(engine) as session:
        statement = select(User).where(User.username == "rmsg")
        user = session.exec(statement).first()
        
        if user:
            print(f"Usuario encontrado: {user.username}")
            nueva_pw = "1234"
            user.hashed_password = get_password_hash(nueva_pw)
            
            session.add(user)
            session.commit()
            print(f"EXITO: La contraseña de '{user.username}' ahora es '{nueva_pw}' (encriptada).")
        else:
            print("ERROR: No se encontró al usuario 'rmsg' en la base de datos.")

if __name__ == "__main__":
    reset_admin_password()