from fastapi import FastAPI
from database import create_db_and_tables
from contextlib import asynccontextmanager
from routers import user, route, truck
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crear tablas al iniciar
    create_db_and_tables()
    yield
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

# Configuración de CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusión de Routers
# Si user.py tiene prefix="/users", la ruta será /users/token
app.include_router(user.router)
app.include_router(route.router)
app.include_router(truck.router)

@app.get("/")
async def root():
    return {"status": "online", "message": "TMS API Working"}