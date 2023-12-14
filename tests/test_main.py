import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db
from database import Base
from fastapi.testclient import TestClient

load_dotenv()
engine = create_engine(os.getenv('TESTING_DATABASE_URL'))
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_get_weather_status_code():
    response = client.get('/api/weather/')
    assert response.status_code == 200


def test_get_weather_response_without_query_params():
    response = client.get('/api/weather/')
    assert response.json() == {"count": 9, "data": [
        {"station_id": 1, "max_temperature": 203, "min_temperature": 103, "precipitation": 22, "date": "2023-01-01"},
        {"station_id": 1, "max_temperature": 253, "min_temperature": 133, "precipitation": 562, "date": "2022-11-03"},
        {"station_id": 1, "max_temperature": 453, "min_temperature": 232, "precipitation": 121, "date": "2002-11-23"},
        {"station_id": 2, "max_temperature": 452, "min_temperature": 46, "precipitation": 345, "date": "2012-04-13"},
        {"station_id": 2, "max_temperature": 35, "min_temperature": 4, "precipitation": 243, "date": "2011-06-03"},
        {"station_id": 2, "max_temperature": 35, "min_temperature": 4, "precipitation": 243, "date": "2001-01-01"},
        {"station_id": 3, "max_temperature": 45, "min_temperature": 4, "precipitation": 243, "date": "2002-01-01"},
        {"station_id": 3, "max_temperature": 45, "min_temperature": 4, "precipitation": 243, "date": "2004-01-01"},
        {"station_id": 3, "max_temperature": 45, "min_temperature": 4, "precipitation": 243, "date": "2006-01-01"}]}


def test_get_weather_response_with_one_query_params():
    response1 = client.get('/api/weather/?station_id=1')
    response2 = client.get('/api/weather/?date=2006-01-01')
    assert response1.json() == {"count": 3, "data": [
        {"station_id": 1, "max_temperature": 203, "min_temperature": 103, "precipitation": 22, "date": "2023-01-01"},
        {"station_id": 1, "max_temperature": 253, "min_temperature": 133, "precipitation": 562, "date": "2022-11-03"},
        {"station_id": 1, "max_temperature": 453, "min_temperature": 232, "precipitation": 121, "date": "2002-11-23"}]}
    assert response2.json() == {"count": 1, "data": [{"station_id": 3, "max_temperature": 45, "min_temperature": 4,
                                                      "precipitation": 243, "date": "2006-01-01"}]}


def test_get_weather_response_with_two_query_params():
    response1 = client.get('/api/weather/?station_id=1&date=2022-11-03')
    response2 = client.get('/api/weather/?date=2022-01-01&station_id=12')
    assert response1.json() == {"count": 1, "data": [{"station_id": 1, "max_temperature": 253, "min_temperature": 133,
                                                      "precipitation": 562, "date": "2022-11-03"}]}
    assert response2.json() == {'count': 0, 'data': []}


def test_get_weather_response_pagination():
    response = client.get('/api/weather/?page=1&limit=2')
    assert response.json().get('count') == 2


def test_get_stats_status_code():
    response = client.get('/api/weather/stats/')
    assert response.status_code == 200


def test_get_stats_response_without_query_params():
    response = client.get('/api/weather/stats')
    assert response.json() == {"count": 3, "data": [
        {"avg_min_temperature": 0, "avg_precipitation": 24, "station_id": 3, "avg_max_temperature": 4},
        {"avg_min_temperature": 1.3333333333333333, "avg_precipitation": 27.333333333333332, "station_id": 2,
         "avg_max_temperature": 17},
        {"avg_min_temperature": 15.333333333333334, "avg_precipitation": 23.333333333333332, "station_id": 1,
         "avg_max_temperature": 30}]}


def test_all_records_response_with_params():
    response = client.get('/api/weather/stats/?station_id=1')
    assert response.json() == {"count": 1, "data": [
        {"avg_min_temperature": 15.333333333333334, "avg_precipitation": 23.333333333333332, "station_id": 1,
         "avg_max_temperature": 30.0}]}


def test_all_records_response_pagination():
    response = client.get('/api/weather/stats/?page=0&limit=3')
    assert response.json().get('count') == 3
