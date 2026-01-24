import os
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURACIÓN DE JWT ---

# Esta es tu "llave secreta". ¡Debe ser secreta y muy segura!
# Puedes generar una con: openssl rand -hex 32
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # El token expirará en 30 minutos