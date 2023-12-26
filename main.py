from fastapi import FastAPI, Depends, Query
import models
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from typing import Annotated, Optional

app = FastAPI()

'''
This will create db tables
'''
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get('/api/weather')
async def get_weather(db: db_dependency, station_id: Optional[int] = None, date: Optional[str] = None,
                      page: int = Query(0), limit: int = Query(10)):
    try:
        queryset = db.query(models.Record)
        if station_id:
            queryset = queryset.filter(models.Record.station_id == station_id)
        if date:
            queryset = queryset.filter(models.Record.date == date)
        queryset = queryset.offset(page).limit(limit).all()
        return {'count': len(queryset), 'data': queryset}
    except Exception as e:
        return {'error': e}


@app.get('/api/weather/stats')
async def get_stats(db: db_dependency, station_id: Optional[int] = None, year: Optional[int] = None,  page: int = Query(0), limit: int = Query(10)):
    try:
        queryset = db.query(models.Stats)
        if station_id:
            queryset = queryset.filter(models.Stats.station_id == station_id)
        if year:
            queryset = queryset.filter(models.Stats.year == year)

        queryset = queryset.offset(page).limit(limit).all()
        return {'count': len(queryset), 'data': queryset}
    except Exception as e:
        return {'error': e}
