# server/routers/route.py
from fastapi import APIRouter, Depends
# IMPORTANTE: Aquí faltaba el 'select'
from sqlmodel import Session, select 
from database import get_session
from models import Route
from typing import List

router = APIRouter(
    prefix="/routes",
    tags=["routes"]
)

@router.get("/", response_model=List[Route])
def read_routes(session: Session = Depends(get_session)):
    routes = session.exec(select(Route)).all()
    return routes

@router.post("/", response_model=Route)
def create_route(route: Route, session: Session = Depends(get_session)):
    session.add(route)
    session.commit()
    session.refresh(route)
    return route