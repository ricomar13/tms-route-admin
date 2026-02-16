# server/seed.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import Session
from config.database import engine, create_db_and_tables
from app.models.models import Truck, Route

def seed_data():
    # 0. Primero creamos las tablas nuevas en MariaDB
    print("Verificando y creando tablas...")
    create_db_and_tables()

    with Session(engine) as session:
        print("Insertando datos de prueba...")
        # 1. Crear Camiones (Agregamos capacidad para que coincida con tu modelo)
        t1 = Truck(plate="ABC-123", model="Kenworth T680", capacity=18000, status="disponible")
        t2 = Truck(plate="XYZ-789", model="Volvo FH", capacity=22000, status="en_ruta")
        
        session.add(t1)
        session.add(t2)
        session.flush() # Esto asigna IDs a los camiones antes de seguir

        # 2. Crear Rutas (Ejemplo México)
        r1 = Route(
            name="Ruta Centro-Sur",
            origin_name="CDMX", origin_lat=19.4326, origin_lng=-99.1332,
            destination_name="Tuxtla Gutiérrez", destination_lat=16.7569, destination_lng=-93.1292,
            status="en_transito", 
            truck_id=t2.id # Usamos el ID del camión Volvo
        )
        
        session.add(r1)
        session.commit()
        print("¡Todo listo! Datos insertados en MariaDB.")

if __name__ == "__main__":
    seed_data()