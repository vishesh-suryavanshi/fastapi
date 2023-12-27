# Weather API with fastAPI.
There are 3 endpoints in this project:-
  1. `/api/weather/`
  2. `/api/weather/stats/`
  3. `/api/docs`

# Project Setup and Installation.
1. Clone the git repository.
2. Create and activate a virtual environment using the below commands:-
  - `pip install virtualenv`
  - `python -m venv env`
  - `source env/bin/activate`
3. Run the below command to install the required packages:-
  - `pip install -r requirements.txt`

# Setup environment variables.
Create a .env file and store your database credentials in below format:-
  - `dbname = 'name_of_db'`
  - `user= 'username_of_db'`
  - `password= 'password_of_db'`
  - `host= 'host_of_db'`
  - `port' =  'port_no_of_db'`
  - `MAIN_DATABASE_URL = 'url_of_main_db'`

# Run project.
1. Use `data_script.py` and `stats_script.py` file to dump the database using below commands:-
  - `python data_script.py`
  - `python stats_script.py`
2. Run the below command to run the project:-
  - `uvicorn main:app --reload`

# To access the API endpoints:
  - `/api/weather/`  -- for weather records
  - `/api/weather/stats/`  -- for weather stats
  - `api/docs` -- for swagger documentation

# Testing.
To run the testcases use this command:-
  - `pytest`
