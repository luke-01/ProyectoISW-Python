from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
import controller as ctrl
from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)
app = FastAPI()


def getDB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/proyectos", response_model=List[schemas.Proyecto])
def obtener_proyectos(db: Session = Depends(getDB)):
    return ctrl.getProyectos(db)


@app.get("/proyectos/{id_proyecto}", response_model=schemas.Proyecto)
def obtener_proyecto_por_id(id_proyecto: int, db: Session = Depends(getDB)):
    proyecto = ctrl.getProyecto(id_proyecto, db)
    if proyecto is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return proyecto


@app.post("/proyectos", response_model=schemas.Proyecto)
def crear_proyecto(item: schemas.CrearProyecto, db: Session = Depends(getDB)):
    proyecto = ctrl.createProyecto(item, db)
    if proyecto is None:
        raise HTTPException(status_code=400, detail="Maker asociado no existe")
    else:
        return proyecto


@app.put("/proyectos/{id_proyecto}", response_model=schemas.Proyecto)
def actualizar_proyecto(id_proyecto: int, item: schemas.ActualizarProyecto, db: Session = Depends(getDB)):
    proyecto, status = ctrl.updateProyecto(id_proyecto, item, db)
    if proyecto is None:
        if status == 1:
            raise HTTPException(status_code=400, detail="Maker asociado no existe")
        elif status == 2:
            raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return proyecto


@app.delete("/proyectos/{id_proyecto}", response_model=None)
def eliminar_proyecto(id_proyecto: int, db: Session = Depends(getDB)):
    proyecto = ctrl.deleteProyecto(id_proyecto, db)
    if proyecto is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return {}

# =======================SESIONES=========================

@app.get("/sesiones", response_model=List[schemas.Sesion])
def obtener_sesiones(db: Session = Depends(getDB)):
    return ctrl.getSesiones(db)


@app.get("/sesiones/{id_sesion}", response_model=schemas.Sesion)
def obtener_sesion_por_id(id_sesion: int, db: Session = Depends(getDB)):
    sesion = ctrl.getSesion(id_sesion, db)
    if sesion is None:
        raise HTTPException(status_code=404, detail="Sesion no encontrada")
    return sesion


@app.post("/sesiones", response_model=schemas.Sesion)
def crear_sesion(item: schemas.CrearSesion, db: Session = Depends(getDB)):
    try:
        return ctrl.createSesion(item, db)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Proyecto asociado no existe")


@app.put("/sesiones/{id_sesion}", response_model=schemas.Sesion)
def actualizar_sesion(id_sesion: int, item: schemas.ActualizarSesion, db: Session = Depends(getDB)):
    try:
        sesion = ctrl.updateSesion(id_sesion, item, db)
        if sesion is None:
            raise HTTPException(status_code=404, detail="Sesion no encontrada")
        return sesion
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Proyecto asociado no existe")


@app.delete("/sesiones/{id_sesion}", response_model=None)
def eliminar_sesion(id_sesion: int, db: Session = Depends(getDB)):
    sesion = ctrl.deleteSesion(id_sesion, db)
    if sesion is None:
        raise HTTPException(status_code=404, detail="sesion no encontrada")
    return {}

# =======================RESERVAS=========================

@app.get("/reservas", response_model=List[schemas.Reserva])
def obtener_reservas(db: Session = Depends(getDB)):
    return ctrl.getReservas(db)


@app.get("/reservas/{id_reserva}", response_model=schemas.Reserva)
def obtener_reserva_por_id(id_reserva: int, db: Session = Depends(getDB)):
    reserva = ctrl.getReserva(id_reserva, db)
    if reserva is None:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return reserva


@app.post("/reservas", response_model=schemas.Reserva)
def crear_reserva(item: schemas.CrearReserva, db: Session = Depends(getDB)):
    try:
        return ctrl.createReserva(item, db)
    except IntegrityError as e:
        if "UniqueViolation" in e.args[0]:
            raise HTTPException(status_code=400, detail="Reserva no posible")
        else:
            raise HTTPException(status_code=400, detail="Sesion asociada no existe")


@app.put("/reservas/{id_reserva}", response_model=schemas.Reserva)
def actualizar_reserva(id_reserva: int, item: schemas.ActualizarReserva, db: Session = Depends(getDB)):
    try:
        reserva = ctrl.updateReserva(id_reserva, item, db)
        if reserva is None:
            raise HTTPException(status_code=404, detail="Reserva no encontrada")
        return reserva
    except IntegrityError as e:
        if "UniqueViolation" in e.args[0]:
            raise HTTPException(status_code=400, detail="Reserva no posible")
        else:
            raise HTTPException(status_code=400, detail="Sesion asociada no existe")


@app.delete("/reservas/{id_reserva}", response_model=None)
def eliminar_reserva(id_reserva: int, db: Session = Depends(getDB)):
    reserva = ctrl.deleteReserva(id_reserva, db)
    if reserva is None:
        raise HTTPException(status_code=404, detail="reserva no encontrada")
    return {}
