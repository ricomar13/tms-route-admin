# server/routers/truck.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import Truck
from typing import List

router = APIRouter(prefix="/trucks", tags=["trucks"])

@router.get("/", response_model=List[Truck])
def read_trucks(session: Session = Depends(get_session)):
    # Trae todos los camiones registrados en la base de datos
    return session.exec(select(Truck)).all()

@router.post("/", response_model=Truck)
def create_truck(truck: Truck, session: Session = Depends(get_session)):
    # Guarda el nuevo camión en MariaDB
    session.add(truck)
    session.commit()
    session.refresh(truck)
    return truck