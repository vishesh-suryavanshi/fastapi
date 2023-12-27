from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date, PrimaryKeyConstraint
from database import Base


class Station(Base):
    __tablename__ = 'station'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Record(Base):
    __tablename__ = 'record'
    date = Column(Date)
    max_temperature = Column(Integer)
    min_temperature = Column(Integer)
    precipitation = Column(Integer)
    station_id = Column(Integer, ForeignKey('station.id'))
    __table_args__ = (
        PrimaryKeyConstraint(
            date,
            station_id
        ),
    )


class Stats(Base):
    __tablename__ = 'stats'
    avg_max_temperature = Column(Float)
    avg_min_temperature = Column(Float)
    total_precipitation = Column(Float)
    year = Column(Integer)
    station_id = Column(Integer, ForeignKey('station.id'))
    __table_args__ = (
        PrimaryKeyConstraint(
            year,
            station_id
        ),
    )
