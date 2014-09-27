from sqlalchemy import create_engine, Column, Integer, String, Date, \
    DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

import settings


DeclarativeBase = declarative_base()

def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))


def create_proyecto_table(engine):
    DeclarativeBase.metadata.create_all(engine)


class Proyecto(DeclarativeBase):
    """our table model using Sqlalchemy."""
    __tablename__ = "pdl_proyecto"

    id = Column('id', Integer, primary_key=True)
    codigo = Column('codigo', String(20))
    numero_proyecto = Column('numero_proyecto', String(50))
    short_url = Column('short_url', String(20))
    congresistas = Column('congresistas', Text)

    # migrate from date as string
    fecha_presentacion = Column('fecha_presentacion', Date)
    titulo = Column('titulo', Text)
    expediente = Column('expediente', String(200))
    pdf_url = Column('pdf_url', String(200))
    seguimiento_page = Column('seguimiento_page', String(200))

    # migrate from timestamp field
    time_created = Column('time_created', DateTime)
    time_edited = Column('time_edited', DateTime)
