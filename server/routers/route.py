from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select 
from database import get_session
from models import Route, Truck
from typing import List

router = APIRouter(prefix="/routes", tags=["routes"])

@router.get("/", response_model=List[Route])
def read_routes(session: Session = Depends(get_session)):
    return session.exec(select(Route)).all()

@router.post("/", response_model=Route)
def create_route(route: Route, session: Session = Depends(get_session)):
    session.add(route)
    session.commit()
    session.refresh(route)
    return route

@router.delete("/{route_id}")
def delete_route(route_id: int, session: Session = Depends(get_session)):
    route = session.get(Route, route_id)
    if not route:
        raise HTTPException(status_code=404, detail="No encontrada")
    session.delete(route)
    session.commit()
    return {"ok": True}

@router.patch("/{route_id}", response_model=Route)
def update_route(route_id: int, update_data: dict, session: Session = Depends(get_session)):
    db_route = session.get(Route, route_id)
    if not db_route:
        raise HTTPException(status_code=404, detail="No encontrada")

    old_truck_id = db_route.truck_id
    new_truck_id = update_data.get("truck_id")

    # Sincronización de camiones al reasignar
    if new_truck_id and new_truck_id != old_truck_id:
        new_t = session.get(Truck, new_truck_id)
        if new_t: new_t.status = "en_ruta"
        
        # ¿Queda libre el viejo?
        stmt = select(Route).where(Route.truck_id == old_truck_id, Route.status == "en_transito", Route.id != route_id)
        if not session.exec(stmt).all():
            old_t = session.get(Truck, old_truck_id)
            if old_t: old_t.status = "disponible"

    # Liberar camión al terminar ruta
    if update_data.get("status") == "terminada":
        t_id = new_truck_id or old_truck_id
        stmt = select(Route).where(Route.truck_id == t_id, Route.status == "en_transito", Route.id != route_id)
        if not session.exec(stmt).all():
            t = session.get(Truck, t_id)
            if t: t.status = "disponible"

    for key, value in update_data.items():
        if hasattr(db_route, key): setattr(db_route, key, value)
        
    session.add(db_route)
    session.commit()
    session.refresh(db_route)
    return db_route