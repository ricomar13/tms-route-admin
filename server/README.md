# Administrador de Rutas
Este proyecto en primera entrega sirve como prueba de concepto para un administrador de rutas, que comprende de un loggin de usuario y una vista de menu principal general
---
## 📋 Prerrequisitos
Antes de empezar, se debe tener instalado lo siguiente en tu sistema:
* **Python 3.8+**
* **pip** (el gestor de paquetes de Python)
---
## 🚀 Guía de Instalación y Configuración
Sigue estos pasos para levantar un entorno de desarrollo local.

### 1. Clonar el Repositorio (Opcional)

Si este proyecto está en un repositorio Git, el primer paso es clonarlo. Si no, simplemente crea una carpeta para tu proyecto.

```bash
git clone <url-del-repositorio>
cd <nombre-de-la-carpeta>

# 1. Crea el entorno virtual en una carpeta llamada .venv
python -m venv .venv

# 2. Activa el entorno (el comando varía según tu sistema operativo):

# En Windows (usando PowerShell):
.venv\Scripts\activate

# En macOS y Linux (usando Bash/Zsh):
source .venv/bin/activate

# Todas las librerías de Python necesarias se encuentran listadas en requirements.txt. Para instalarlas todas de una vez, ejecuta::
pip install -r requirements.txt

# Primero, navega a la carpeta bin
cd "C:\Program Files\PostgreSQL\17\bin"

# Luego, inicia el servidor sql
.\pg_ctl -D "C:\Program Files\PostgreSQL\17\data" start

# Run servidor local
fastapi dev main.py 