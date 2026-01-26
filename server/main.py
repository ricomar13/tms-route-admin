from fastapi import FastAPI
from database import create_db_and_tables
from contextlib import asynccontextmanager
from routers import user, route, truck
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    #Load on startup
    create_db_and_tables()
    yield
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

#    Define los "orígenes" (clientes) que tienen permiso para hablar con tu API.
origins = [
    "http://localhost:5173", # La URL de tu frontend de Vue
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Permite los orígenes en la lista
    allow_credentials=True,
    allow_methods=["*"],         # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],         # Permite todas las cabeceras
)

app.include_router(user.router)
app.include_router(route.router)
app.include_router(truck.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}