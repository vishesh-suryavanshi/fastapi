from fastapi import FastAPI, Depends, Query
import models
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


@app.get('/api/weather')
async def get_weather(db: db_dependency, station_id: Optional[int] = None, date: Optional[str] = None,
                      page: int = Query(0), limit: int = Query(10)):
    """
     Get weather data from the specified station and date.

        Parameters:
        - db (db_dependency): The database dependency to retrieve the weather data.
        - station_id (Optional[int]): The ID of the weather's station. If it is None, data for all stations will be retrieved.
        - date (Optional[str]): The date for which weather data is requested. If None, data for all dates will be retrieved.
        - page (int): The page number for paginated results (default is 0).
        - limit (int): The number of items to return per page (default is 10).

        Returns:
        - Weather data for the specified station and date, paginated according to the provided page and limit.
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

        Parameters:
        - db (db_dependency): The database dependency to retrieve statistical data.
        - station_id (Optional[int]): The ID of the weather station. If None, data for all stations will be retrieved.
        - year (Optional[int]): The year for which statistical data is requested. If it is None, data for all years will be retrieved.
        - page (int): The page number for paginated results (default is 0).
        - limit (int): The number of items to return per page (default is 10).

        Returns:
        - Statistical data for the specified weather station and year, paginated according to the provided page and limit.
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
