# server/reset_pw.py
from sqlmodel import Session, select
from database import engine
from models import User
from security import get_password_hash

def reset_admin_password():
    with Session(engine) as session:
        # Buscamos a tu usuario por el username que nos pasaste
        statement = select(User).where(User.username == "rmsg")
        user = session.exec(statement).first()
        
        if user:
            print(f"Usuario encontrado: {user.username}")
            # Encriptamos la nueva contraseña correctamente
            nueva_pw = "1234"
            user.hashed_password = get_password_hash(nueva_pw)
            
            session.add(user)
            session.commit()
            print(f"EXITO: La contraseña de '{user.username}' ahora es '{nueva_pw}' (encriptada).")
        else:
            print("ERROR: No se encontró al usuario 'rmsg' en la base de datos.")

if __name__ == "__main__":
    reset_admin_password()