Transport Management System (TMS) - Visualización de Rutas
Este proyecto es una plataforma web diseñada para la gestión y visualización de rutas de transporte optimizadas. Cuenta con una arquitectura desacoplada con un backend en FastAPI (Python) y un frontend en Vue.js + Quasar (JavaScript).

Requisitos Previos
Antes de comenzar, asegúrate de tener instalado lo siguiente:

Python 3.12+ (Asegúrate de marcar "Add Python to PATH" durante la instalación).

Node.js LTS (Incluye npm).

PostgreSQL (Servidor de base de datos activo).

Git.

Configuración del Repositorio (Entorno de Trabajo)

Bash
# 1. Clonar el proyecto
git clone https://github.com/ricomar13/tms-route-admin.git

cd tms-route-admin

# 2. Configurar identidad local
git config user.name "Tu Nombre"
git config user.email "tu-correo@personal.com"

Backend:
El backend maneja la lógica de negocio, seguridad JWT y la conexión a la base de datos PostgreSQL.

Comandos a ejecutar en la carpeta raíz clonada:
1. Preparar el entorno virtual
# puede tardar un poco

Bash

-------------------
cd server 
python -m venv .venv
-------------------

2. Activar el entorno virtual
Git Bash (Windows): 

-------------------------------------
source .venv/Scripts/activate
-------------------------------------

PowerShell: 

# Si hay problemas de permisos en powerShell ejecuta antes en la terminal:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

-------------------------------------
.\.venv\Scripts\Activate.ps1
-------------------------------------

CMD: 

-------------------------------------
.\venv\Scripts\activate.bat
-------------------------------------


3. Instalar dependencias
Bash

-------------------------------------
pip install -r requirements.txt
-------------------------------------

4. Variables de Entorno
Crea un archivo llamado .env dentro de la carpeta server/ y configura tus credenciales:

DATABASE_URL=postgresql://usuario:password@localhost:5432/nombre_db
SECRET_KEY=tu_llave_secreta_para_jwt
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30


5. Ejecutar el servidor
Bash
--------------------
fastapi dev main.py
-------------------


Configuración del Frontend (route-admin)
El frontend es una Single Page Application (SPA) construida con Quasar para una interfaz moderna y reactiva.

1. Instalar librerías
Bash

-------------------
cd ../route-admin
npm install
-------------------

2. Variables de Entorno
Si el frontend requiere conectar a una URL específica, crea un archivo .env en la raíz de route-admin/:

VITE_API_URL=http://127.0.0.1:8000


3. Ejecutar en modo desarrollo
Bash


----------------
npm run dev
-----------------
Acceso local: http://localhost:5173

Estructura del Proyecto
/server: API REST construida con FastAPI, SQLModel para el ORM y validación de tipos con Pydantic.

/route-admin: Interfaz de usuario con Quasar Framework, Axios para el consumo de servicios y Vue Router para la navegación.

 Notas de Desarrollo
Seguridad: Los commits deben realizarse siempre verificando que archivos sensibles como .env o carpetas pesadas como node_modules y .venv estén correctamente listados en el .gitignore.

Flujo de Git:

Bash
--------------------------------------------------
git add .
git commit -m "Descripción clara del cambio"
git push origin main
--------------------------------------------------