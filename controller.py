from sqlalchemy.orm import Session
import models
import schemas
import requests


user_endpoint = "http://ec2-3-13-79-51.us-east-2.compute.amazonaws.com:8081"


def getProyectos(db: Session):
    return db.query(models.Proyecto).all()


def getProyecto(id_proyecto: int, db: Session):
    return db.query(models.Proyecto).filter(models.Proyecto.id == id_proyecto).first()


def createProyecto(item: schemas.CrearProyecto, db: Session):
    maker = requests.get(f"{user_endpoint}/persona/{item.id_maker}")
    if "message" in maker.json():
        return None
    proyecto = models.Proyecto(nombre=item.nombre,
                               descripcion=item.descripcion,
                               id_maker=item.id_maker)
    db.add(proyecto)
    db.commit()
    db.refresh(proyecto)
    return proyecto


def updateProyecto(id_proyecto: int, item: schemas.ActualizarProyecto, db: Session):
    maker = requests.get(f"{user_endpoint}/persona/{item.id_maker}")
    if "message" in maker.json():
        return (None, 1)
    proyecto = db.query(models.Proyecto).filter(models.Proyecto.id == id_proyecto).first()
    if proyecto is None:
        return (None, 2)
    proyecto.nombre = item.nombre
    proyecto.descripcion = item.descripcion
    proyecto.id_maker = item.id_maker
    db.add(proyecto)
    db.commit()
    db.refresh(proyecto)
    return proyecto


def deleteProyecto(id_proyecto: int, db: Session):
    proyecto = db.query(models.Proyecto).filter(models.Proyecto.id == id_proyecto).first()
    if proyecto is None:
        return None
    db.delete(proyecto)
    db.commit()
    return proyecto

# ================SESIONES========================

def getSesiones(db: Session):
    return db.query(models.Sesion).all()


def getSesion(id_sesion: int, db: Session):
    return db.query(models.Sesion).filter(models.Sesion.id == id_sesion).first()


def createSesion(item: schemas.CrearSesion, db: Session):
    sesion = models.Sesion(cumplida=item.cumplida,
                           id_proyecto=item.id_proyecto)
    db.add(sesion)
    db.commit()
    db.refresh(sesion)
    return sesion


def updateSesion(id_sesion: int, item: schemas.ActualizarSesion, db: Session):
    sesion = db.query(models.Sesion).filter(models.Sesion.id == id_sesion).first() 
    if sesion is None:
        return None
    sesion.cumplida = item.cumplida
    sesion.id_proyecto = item.id_proyecto
    db.add(sesion)
    db.commit()
    db.refresh(sesion)
    return sesion


def deleteSesion(id_sesion: int, db: Session):
    sesion = db.query(models.Sesion).filter(models.Sesion.id == id_sesion).first() 
    if sesion is None:
        return None
    db.delete(sesion)
    db.commit()
    return sesion

# ================RESERVAS========================

def getReservas(db: Session):
    return db.query(models.Reserva).all()


def getReserva(id_reserva: int, db: Session):
    return db.query(models.Reserva).filter(models.Reserva.id == id_reserva).first()


def createReserva(item: schemas.CrearReserva, db: Session):
#datetime.strptime('2021-08-01 13:00:00', '%Y-%m-%d %X')
    reserva = models.Reserva(timestamp=item.timestamp,
                             id_maquina=item.id_maquina,
                             id_sesion=item.id_sesion)
    db.add(reserva)
    db.commit()
    db.refresh(reserva)
    return reserva


def updateReserva(id_reserva: int, item: schemas.ActualizarReserva, db: Session):
    reserva = db.query(models.Reserva).filter(models.Reserva.id == id_reserva).first() 
    if reserva is None:
        return None
    reserva.timestamp = item.timestamp
    reserva.id_maquina = item.id_maquina
    reserva.id_sesion = item.id_sesion
    db.add(reserva)
    db.commit()
    db.refresh(reserva)
    return reserva


def deleteReserva(id_reserva: int, db: Session):
    reserva = db.query(models.Reserva).filter(models.Reserva.id == id_reserva).first() 
    if reserva is None:
        return None
    db.delete(reserva)
    db.commit()
    return reserva

