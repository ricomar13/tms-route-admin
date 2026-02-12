from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import Truck, Route
from typing import List

router = APIRouter(prefix="/trucks", tags=["trucks"])

@router.get("/", response_model=List[Truck])
def read_trucks(session: Session = Depends(get_session)):
    return session.exec(select(Truck)).all()

@router.post("/", response_model=Truck)
def create_truck(truck: Truck, session: Session = Depends(get_session)):
    session.add(truck)
    session.commit()
    session.refresh(truck)
    return truck

@router.patch("/{truck_id}", response_model=Truck)
def update_truck(truck_id: int, update_data: dict, session: Session = Depends(get_session)):
    db_truck = session.get(Truck, truck_id)
    if not db_truck:
        raise HTTPException(status_code=404, detail="No existe la unidad")
    
    # VALIDACIÓN: No permitir 'disponible' si tiene ruta activa
    if update_data.get("status") == "disponible":
        active_route = session.exec(
            select(Route).where(Route.truck_id == truck_id, Route.status == "en_transito")
        ).first()
        if active_route:
            raise HTTPException(
                status_code=400, 
                detail=f"No se puede poner disponible. Tiene una ruta activa: {active_route.name}"
            )
    
    for key, value in update_data.items():
        if hasattr(db_truck, key):
            setattr(db_truck, key, value)
            
    session.add(db_truck)
    session.commit()
    session.refresh(db_truck)
    return db_truck

@router.delete("/{truck_id}")
def delete_truck(truck_id: int, session: Session = Depends(get_session)):
    truck = session.get(Truck, truck_id)
    if not truck:
        raise HTTPException(status_code=404, detail="No existe")
    
    # VALIDACIÓN: No permitir borrar si tiene ruta activa
    active_route = session.exec(
        select(Route).where(Route.truck_id == truck_id, Route.status == "en_transito")
    ).first()
    if active_route:
        raise HTTPException(status_code=400, detail="No se puede eliminar un camión con ruta activa")

    session.delete(truck)
    session.commit()
    return {"ok": True}