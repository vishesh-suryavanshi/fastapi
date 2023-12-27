import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from main import app, get_db
from fastapi.testclient import TestClient
from database import SessionLocal

load_dotenv()
engine = create_engine(os.getenv('TESTING_DATABASE_URL'))
TestingSessionLocal = SessionLocal


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_get_weather_with_no_filter():
    response = client.get('/api/weather/')
    assert response.status_code == 200
    assert response.json()['count'] == 10


def test_get_weather_response_with_station_id_filter():
    response = client.get('/api/weather/?station_id=1')
    assert response.status_code == 200
    assert response.json()['data'][0]['station_id'] == 1

def test_get_weather_response_with_date_filter():
    response = client.get('/api/weather/?date=1985-01-01')
    assert response.status_code == 200
    assert response.json()['data'][0]['date'] == '1985-01-01'


def test_get_weather_response_with_both_filters():
    response = client.get('/api/weather/?station_id=1&date=2010-03-02')
    assert response.status_code == 200
    assert response.json()['data'][0]['date'] == '2010-03-02'
    assert response.json()['data'][0]['station_id'] == 1


def test_get_weather_response_pagination():
    response = client.get('/api/weather/?page=1&limit=2')
    assert response.status_code == 200
    assert response.json()['count'] == 2


def test_get_stats_without_filter():
    response = client.get('/api/weather/stats/')
    assert response.status_code == 200
    assert response.json()['count'] == 10


def test_get_stats_response_with_station_id_filter():
    response = client.get('/api/weather/stats?station_id=3')
    assert response.status_code == 200
    assert response.json()['count'] == 10
    assert response.json()['data'][0]['station_id'] == 3


def test_all_records_response_with_year_filter():
    response = client.get('/api/weather/stats/?year=1999')
    assert response.status_code == 200
    assert response.json()['count'] == 10
    assert response.json()['data'][0]['year'] == 1999


def test_all_records_response_with_both_filters():
    response = client.get('/api/weather/stats/?year=2006&station_id=3')
    assert response.status_code == 200
    assert response.json()['count'] == 1
    assert response.json()['data'][0]['year'] == 2006
    assert response.json()['data'][0]['station_id'] == 3



def test_all_records_response_pagination():
    response = client.get('/api/weather/stats/?page=0&limit=3')
    assert response.json()['count'] == 3
