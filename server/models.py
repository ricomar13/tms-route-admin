from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import EmailStr
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # Columnas en la base de datos
    user_code: Optional[str] = Field(default=None, unique=True, index=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str 
    first_name: str
    middle_name: Optional[str] = Field(default=None)
    last_name: str
    second_last_name: Optional[str] = Field(default=None)
    email: EmailStr = Field(unique=True, index=True)
    role: Optional[str] = Field(default=None, index=True)

    #obtener el nombre completo.
    @property
    def full_name(self) -> str:
        parts = [self.first_name, self.middle_name, self.last_name, self.second_last_name]
        return " ".join(part for part in parts if part)
    
class Truck(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    plate: str = Field(unique=True, index=True) # Placas del camión
    model: str
    capacity: float # Capacidad en kg o m3
    status: str = Field(default="disponible") # disponible, en_ruta, mantenimiento

    # Relación con las rutas
    routes: List["Route"] = Relationship(back_populates="truck")

class Route(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True) # Ejemplo: "Ruta CDMX - Tuxtla"
    origin_name: str
    origin_lat: float
    origin_lng: float
    destination_name: str
    destination_lat: float
    destination_lng: float
    status: str = Field(default="pendiente") # pendiente, en_transito, completada
    
    # Llave foránea para el camión
    truck_id: Optional[int] = Field(default=None, foreign_key="truck.id")
    truck: Optional[Truck] = Relationship(back_populates="routes")