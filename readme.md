# Transport Management System (TMS) - Route Admin

Este proyecto es una plataforma integral para la gestión y visualización de rutas de transporte, diseñada con una arquitectura modular y escalable. El sistema permite el control total de la flota, el monitoreo de trayectos en tiempo real y la administración avanzada de perfiles de usuario.

---

## Arquitectura del Proyecto

El backend está organizado siguiendo el patrón de Separación de Responsabilidades para garantizar un código limpio y mantenible:

* **app/controllers**: Define los endpoints de la API y gestiona las peticiones/respuestas HTTP.
* **app/services**: Contiene la lógica de negocio central (Service Layer), como la validación de estados y la persistencia compleja.
* **app/models**: Define las entidades de la base de datos (User, Truck, Route) utilizando SQLModel.
* **app/serializers**: Esquemas de validación Pydantic para asegurar la integridad de los datos de entrada y salida.
* **config/**: Centraliza la configuración de seguridad (JWT/Bcrypt) y la conexión a la base de datos.
* **bin/**: Scripts de utilidad para mantenimiento, reset de credenciales y poblado de datos iniciales.

---

## Características Clave

* **Gestión de Flota**: Control de disponibilidad de camiones con bloqueos automáticos para unidades con rutas activas.
* **Monitoreo de Rutas**: Creación y actualización de trayectos integrados con mapas interactivos (Leaflet).
* **Seguridad**: Autenticación robusta basada en JWT y un sistema de edición de perfil con re-autenticación obligatoria tras cambios de clave.
* **Sincronización de Estados**: El sistema libera automáticamente las unidades al completar o reasignar viajes.

---

## Prerrequisitos

* **Python 3.13+**
* **Node.js LTS** (incluye npm)
* **MariaDB 10.11+** (o XAMPP) activo.
* **Git**

---

# Instalación y Configuración

### 1. Clonar el Proyecto

bash
git clone [https://github.com/ricomar13/tms-route-admin.git](https://github.com/ricomar13/tms-route-admin.git)
cd tms-route-admin

# Configuración del Backend
Navega a la carpeta del servidor y prepara tu entorno virtual:

PowerShell
cd server
python -m venv .venv

# Activar entorno (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt


# Variables de Entorno (.env)
Crea un archivo .env dentro de la carpeta server/ con la siguiente configuración para MariaDB:

DATABASE_URL=mysql+pymysql://usuario:password@localhost:3306/tms_db
SECRET_KEY=tu_llave_secreta_para_jwt
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Configuración del Frontend
En una nueva terminal (desde la raíz del proyecto), instala las librerías necesarias:

Bash
npm install
Ejecución del Sistema
Iniciar Backend (FastAPI)
Asegúrate de tener iniciado el servicio de MariaDB antes de arrancar el servidor:

Bash
cd server
fastapi dev main.py
Acceso a documentación interactiva: http://localhost:8000/docs


# Iniciar Frontend (Vue/Quasar)
Bash
npm run dev
Acceso local: http://localhost:5173

Scripts de Utilidad (bin/)
El sistema incluye herramientas para agilizar el desarrollo y mantenimiento:

## Poblar base de datos con datos de prueba:

Bash
python bin/seed.py
Resetear contraseña de administrador (emergencia):

Bash
python bin/reset_pw.py

### Notas de Desarrollo
* CORS: El backend está configurado para permitir peticiones desde localhost:5173. Para evitar errores de red, asegúrate de utilizar siempre localhost en el navegador y no la IP 127.0.0.1.

* Seguridad: El archivo .env contiene credenciales sensibles y nunca debe ser subido al repositorio público. Verifique que esté correctamente listado en su archivo .gitignore.