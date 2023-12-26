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


def test_get_weather_status_code():
    response = client.get('/api/weather/')
    assert response.status_code == 200


def test_get_weather_response_without_query_params():
    response = client.get('/api/weather/')
    assert response.json() == {'count': 10, 'data': [
        {'precipitation': 56, 'date': '2002-01-30', 'max_temperature': 222, 'min_temperature': 67, 'station_id': 1},
        {'precipitation': 0, 'date': '1986-11-13', 'max_temperature': -44, 'min_temperature': -111, 'station_id': 1},
        {'precipitation': 0, 'date': '1991-04-06', 'max_temperature': 256, 'min_temperature': 94, 'station_id': 1},
        {'precipitation': 0, 'date': '1999-03-18', 'max_temperature': 217, 'min_temperature': 33, 'station_id': 1},
        {'precipitation': 173, 'date': '2000-12-16', 'max_temperature': 72, 'min_temperature': -33, 'station_id': 1},
        {'precipitation': 0, 'date': '2009-08-16', 'max_temperature': 328, 'min_temperature': 167, 'station_id': 1},
        {'precipitation': 0, 'date': '2005-08-27', 'max_temperature': 317, 'min_temperature': 233, 'station_id': 1},
        {'precipitation': 0, 'date': '1995-04-01', 'max_temperature': 94, 'min_temperature': -33, 'station_id': 1},
        {'precipitation': 0, 'date': '2002-03-22', 'max_temperature': 106, 'min_temperature': -61, 'station_id': 1},
        {'precipitation': 0, 'date': '2006-12-29', 'max_temperature': 144, 'min_temperature': 17, 'station_id': 1}]}


def test_get_weather_response_with_one_query_params():
    response1 = client.get('/api/weather/?station_id=1')
    response2 = client.get('/api/weather/?date=2006-01-01')
    assert response1.json() == {'count': 10, 'data': [
        {'station_id': 1, 'max_temperature': 222, 'min_temperature': 67, 'date': '2002-01-30', 'precipitation': 56},
        {'station_id': 1, 'max_temperature': -44, 'min_temperature': -111, 'date': '1986-11-13', 'precipitation': 0},
        {'station_id': 1, 'max_temperature': 256, 'min_temperature': 94, 'date': '1991-04-06', 'precipitation': 0},
        {'station_id': 1, 'max_temperature': 217, 'min_temperature': 33, 'date': '1999-03-18', 'precipitation': 0},
        {'station_id': 1, 'max_temperature': 72, 'min_temperature': -33, 'date': '2000-12-16', 'precipitation': 173},
        {'station_id': 1, 'max_temperature': 328, 'min_temperature': 167, 'date': '2009-08-16', 'precipitation': 0},
        {'station_id': 1, 'max_temperature': 317, 'min_temperature': 233, 'date': '2005-08-27', 'precipitation': 0},
        {'station_id': 1, 'max_temperature': 94, 'min_temperature': -33, 'date': '1995-04-01', 'precipitation': 0},
        {'station_id': 1, 'max_temperature': 106, 'min_temperature': -61, 'date': '2002-03-22', 'precipitation': 0},
        {'station_id': 1, 'max_temperature': 144, 'min_temperature': 17, 'date': '2006-12-29', 'precipitation': 0}]}
    assert response2.json() == {'count': 10, 'data': [
        {'max_temperature': None, 'min_temperature': None, 'station_id': 1, 'precipitation': 0, 'date': '2006-01-01'},
        {'max_temperature': 106, 'min_temperature': -22, 'station_id': 2, 'precipitation': 0, 'date': '2006-01-01'},
        {'max_temperature': 50, 'min_temperature': 6, 'station_id': 3, 'precipitation': 0, 'date': '2006-01-01'},
        {'max_temperature': 61, 'min_temperature': -11, 'station_id': 4, 'precipitation': 28, 'date': '2006-01-01'},
        {'max_temperature': 61, 'min_temperature': -22, 'station_id': 5, 'precipitation': 0, 'date': '2006-01-01'},
        {'max_temperature': 22, 'min_temperature': -11, 'station_id': 7, 'precipitation': 0, 'date': '2006-01-01'},
        {'max_temperature': 22, 'min_temperature': 6, 'station_id': 8, 'precipitation': 0, 'date': '2006-01-01'},
        {'max_temperature': 28, 'min_temperature': -11, 'station_id': 9, 'precipitation': 8, 'date': '2006-01-01'},
        {'max_temperature': 72, 'min_temperature': -17, 'station_id': 10, 'precipitation': 0, 'date': '2006-01-01'},
        {'max_temperature': 17, 'min_temperature': -11, 'station_id': 12, 'precipitation': 0, 'date': '2006-01-01'}]}


def test_get_weather_response_with_two_query_params():
    response1 = client.get('/api/weather/?station_id=1&date=2006-01-01')
    response2 = client.get('/api/weather/?date=2022-01-01&station_id=12')
    assert response1.json() == {'count': 1, 'data': [
        {'station_id': 1, 'max_temperature': None, 'min_temperature': None, 'date': '2006-01-01', 'precipitation': 0}]}
    assert response2.json() == {'count': 0, 'data': []}


def test_get_weather_response_pagination():
    response = client.get('/api/weather/?page=1&limit=2')
    assert response.json().get('count') == 2


def test_get_stats_status_code():
    response = client.get('/api/weather/stats/')
    assert response.status_code == 200


def test_get_stats_response_without_query_params():
    response = client.get('/api/weather/stats')
    assert response.json() == {'count': 10, 'data': [
        {'avg_max_temperature': 15.997237569060774, 'avg_min_temperature': 4.223756906077348, 'year': 2014,
         'station_id': 21, 'avg_precipitation': 2.7044198895027622},
        {'avg_max_temperature': 15.787878787878787, 'avg_min_temperature': 4.112947658402204, 'year': 1995,
         'station_id': 9, 'avg_precipitation': 2.0991735537190084},
        {'avg_max_temperature': 15.160714285714286, 'avg_min_temperature': 4.571428571428571, 'year': 2000,
         'station_id': 26, 'avg_precipitation': 2.818452380952381},
        {'avg_max_temperature': 17.312328767123287, 'avg_min_temperature': 6.4082191780821915, 'year': 2007,
         'station_id': 16, 'avg_precipitation': 2.213698630136986},
        {'avg_max_temperature': 17.87945205479452, 'avg_min_temperature': 7.32054794520548, 'year': 1990,
         'station_id': 19, 'avg_precipitation': 3.3013698630136985},
        {'avg_max_temperature': 17.493150684931507, 'avg_min_temperature': 5.032876712328767, 'year': 1986,
         'station_id': 3, 'avg_precipitation': 2.723287671232877},
        {'avg_max_temperature': 15.402203856749312, 'avg_min_temperature': 3.0, 'year': 1991, 'station_id': 28,
         'avg_precipitation': 2.3168044077134984},
        {'avg_max_temperature': 16.102777777777778, 'avg_min_temperature': 6.591666666666667, 'year': 1993,
         'station_id': 19, 'avg_precipitation': 4.455555555555556},
        {'avg_max_temperature': 18.03013698630137, 'avg_min_temperature': 6.273972602739726, 'year': 1986,
         'station_id': 21, 'avg_precipitation': 2.273972602739726},
        {'avg_max_temperature': 16.731638418079097, 'avg_min_temperature': 6.358757062146893, 'year': 1997,
         'station_id': 38, 'avg_precipitation': 2.6045197740112993}]}


def test_all_records_response_with_first_params():
    response = client.get('/api/weather/stats/?station_id=1')
    assert response.json() == {'count': 10, 'data': [
        {'avg_max_temperature': 17.848837209302324, 'avg_min_temperature': 6.3895348837209305, 'year': 1992,
         'avg_precipitation': 2.4069767441860463, 'station_id': 1},
        {'avg_max_temperature': 19.701538461538462, 'avg_min_temperature': 7.895384615384615, 'year': 2002,
         'avg_precipitation': 3.126153846153846, 'station_id': 1},
        {'avg_max_temperature': 20.533519553072626, 'avg_min_temperature': 7.9525139664804465, 'year': 1999,
         'avg_precipitation': 2.4664804469273744, 'station_id': 1},
        {'avg_max_temperature': 16.5, 'avg_min_temperature': 6.5, 'year': 2012, 'avg_precipitation': 13.625,
         'station_id': 1},
        {'avg_max_temperature': 17.78787878787879, 'avg_min_temperature': 9.015151515151516, 'year': 2011,
         'avg_precipitation': 18.954545454545453, 'station_id': 1},
        {'avg_max_temperature': 17.776536312849164, 'avg_min_temperature': 7.092178770949721, 'year': 1993,
         'avg_precipitation': 3.195530726256983, 'station_id': 1},
        {'avg_max_temperature': 23.328358208955223, 'avg_min_temperature': 12.64179104477612, 'year': 2013,
         'avg_precipitation': 1.791044776119403, 'station_id': 1},
        {'avg_max_temperature': 20.257534246575343, 'avg_min_temperature': 8.676712328767124, 'year': 1991,
         'avg_precipitation': 2.682191780821918, 'station_id': 1},
        {'avg_max_temperature': 18.63125, 'avg_min_temperature': 7.6, 'year': 2009, 'avg_precipitation': 2.809375,
         'station_id': 1},
        {'avg_max_temperature': 24.181818181818183, 'avg_min_temperature': 10.666666666666666, 'year': 2005,
         'avg_precipitation': 2.2303030303030305, 'station_id': 1}]}


def test_all_records_response_with_second_params():
    response = client.get('/api/weather/stats/?year=2006')
    assert response.json() == {'count': 10, 'data': [
        {'avg_max_temperature': 15.87945205479452, 'avg_min_temperature': 6.213698630136986, 'year': 2006,
         'station_id': 53, 'avg_precipitation': 2.56986301369863},
        {'avg_max_temperature': 17.724431818181817, 'avg_min_temperature': 6.232954545454546, 'year': 2006,
         'station_id': 40, 'avg_precipitation': 2.0767045454545454},
        {'avg_max_temperature': 18.323204419889503, 'avg_min_temperature': 7.497237569060774, 'year': 2006,
         'station_id': 38, 'avg_precipitation': 3.2430939226519335},
        {'avg_max_temperature': 17.759887005649716, 'avg_min_temperature': 7.483050847457627, 'year': 2006,
         'station_id': 31, 'avg_precipitation': 4.254237288135593},
        {'avg_max_temperature': 16.667582417582416, 'avg_min_temperature': 5.008241758241758, 'year': 2006,
         'station_id': 9, 'avg_precipitation': 2.7857142857142856},
        {'avg_max_temperature': 16.337912087912088, 'avg_min_temperature': 6.195054945054945, 'year': 2006,
         'station_id': 37, 'avg_precipitation': 4.0467032967032965},
        {'avg_max_temperature': 16.823970037453183, 'avg_min_temperature': 6.325842696629214, 'year': 2006,
         'station_id': 8, 'avg_precipitation': 2.1722846441947565},
        {'avg_max_temperature': 16.950413223140497, 'avg_min_temperature': 6.636363636363637, 'year': 2006,
         'station_id': 24, 'avg_precipitation': 2.9421487603305785},
        {'avg_max_temperature': 17.51232876712329, 'avg_min_temperature': 6.098630136986301, 'year': 2006,
         'station_id': 30, 'avg_precipitation': 2.6054794520547944},
        {'avg_max_temperature': 15.95, 'avg_min_temperature': 4.7272727272727275, 'year': 2006, 'station_id': 4,
         'avg_precipitation': 2.9}]}


def test_all_records_response_with_both_params():
    response = client.get('/api/weather/stats/?year=2006&station_id=1')
    assert response.json() == {'count': 1, 'data': [
        {'avg_max_temperature': 19.876288659793815, 'avg_min_temperature': 8.594501718213058, 'year': 2006,
         'avg_precipitation': 3.687285223367698, 'station_id': 1}]}


def test_all_records_response_pagination():
    response = client.get('/api/weather/stats/?page=0&limit=3')
    assert response.json().get('count') == 3
