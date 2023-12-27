from fastapi import FastAPI, Depends, Query

import models
from data_script import calculate_stats_data, load_file_data
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from typing import Annotated, Optional

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def on_startup():
    try:
        db = next(get_db())
        models.Base.metadata.create_all(bind=engine)
        if not (db.query(models.Record).count() or db.query(models.Station).count()):
            load_file_data()
        if not db.query(models.Stats).count():
            calculate_stats_data()
    except Exception as e:
        print(f"Error during data loading: {str(e)}")


@app.on_event("startup")
async def startup():
    on_startup()


@app.get('/api/weather')
async def get_weather(db: db_dependency, station_id: Optional[int] = None, date: Optional[str] = None,
                      page: int = Query(0), limit: int = Query(10)):
    """
       Get weather data from the specified station and date.

       Args:
       - db:The database dependency to retrieve data.
       - station_id:The id of the station.
       - date:The date for which data is requested.
       - page: The page number for paginated results .
       - limit: The number of items to return per page .

       Returns:
       - JSON data of Weather for the specified station and date (if any).
       """
    try:
        queryset = db.query(models.Record)
        if station_id:
            queryset = queryset.filter(models.Record.station_id == station_id)
            if not queryset.count():
                raise ValueError(f'station_id {station_id} does not exist')
        if date:
            queryset = queryset.filter(models.Record.date == date)
            if not queryset.count():
                raise ValueError(f'date {date} does not exist')
        queryset = queryset.offset(page).limit(limit).all()
        return {'count': len(queryset), 'data': queryset}
    except Exception as e:
        return {'error': str(e)}


@app.get('/api/weather/stats')
async def get_stats(db: db_dependency, station_id: Optional[int] = None, year: Optional[int] = None,
                    page: int = Query(0), limit: int = Query(10)):
    """
         Get statistical data for a weather station and a specific year.

        Args :
        - db : The database dependency to retrieve statistical data.
        - station_id: The ID of the weather station.
        - year  The year for which statistical data is requested.
        - page: The page number for paginated results.
        - limit: The number of items to return per page.

        Returns:
        - Statistical data for the specified weather station and year.
    """
    try:
        queryset = db.query(models.Stats)
        if station_id:
            queryset = queryset.filter(models.Stats.station_id == station_id)
            if not queryset.count():
                raise ValueError(f'station_id {station_id} does not exist')
        if year:
            queryset = queryset.filter(models.Stats.year == year)
            if not queryset.count():
                raise ValueError(f'year {year} does not exist')
        queryset = queryset.offset(page).limit(limit).all()
        return {'count': len(queryset), 'data': queryset}
    except Exception as e:
        return {'error': str(e)}
