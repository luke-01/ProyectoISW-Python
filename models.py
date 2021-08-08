from sqlalchemy import Integer, String, DateTime, Boolean
from sqlalchemy import Column, ForeignKey, Index
from sqlalchemy.orm import relationship
from database import Base


class Proyecto(Base):
    __tablename__ = "proyectos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    descripcion = Column(String)
    id_maker = Column(Integer)

    sesiones = relationship("Sesion", back_populates="proyecto")


class Sesion(Base):
    __tablename__ = "sesiones"

    id = Column(Integer, primary_key=True, index=True)
    cumplida = Column(Boolean)
    id_proyecto = Column(Integer, ForeignKey("proyectos.id"))

    proyecto = relationship("Proyecto", back_populates="sesiones")
    reservas = relationship("Reserva", back_populates="sesion")


class Reserva(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime)
    id_maquina = Column(Integer)
    id_sesion = Column(Integer, ForeignKey("sesiones.id"))

    sesion = relationship("Sesion", back_populates="reservas")


Index("reservas_timestamp_maquina_index", Reserva.timestamp, Reserva.id_maquina, unique=True)
