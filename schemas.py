from datetime import datetime
from pydantic import BaseModel


class ProyectoBase(BaseModel):
    nombre: str
    descripcion: str
    id_maker: int


class SesionBase(BaseModel):
    cumplida: bool
    id_proyecto: int


class ReservaBase(BaseModel):
    timestamp: datetime
    id_maquina: int
    id_sesion: int


class Proyecto(ProyectoBase):
    id: int

    class Config:
        orm_mode = True


class Sesion(SesionBase):
    id: int
    proyecto: Proyecto

    class Config:
        orm_mode = True


class Reserva(ReservaBase):
    id: int
    sesion: Sesion

    class Config:
        orm_mode = True


class CrearProyecto(ProyectoBase):
    pass


class CrearSesion(SesionBase):
    pass


class CrearReserva(ReservaBase):
    pass


class ActualizarProyecto(ProyectoBase):
    pass


class ActualizarSesion(SesionBase):
    pass


class ActualizarReserva(ReservaBase):
    pass
