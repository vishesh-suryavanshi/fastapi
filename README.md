# Weather API with fastAPI.
There are 3 endpoints in this project:-
  1. `/api/weather/`
  2. `/api/weather/stats/`
  3. `/docs`

# Project Setup and Installation.
1. Clone the git repository.
2. Create and activate a virtual environment using the below commands:-
  - `pip install virtualenv`
  - `python -m venv env`
  - `source env/bin/activate` (For Mac and Linux)
  - `env\Scripts\activate` (in Windows)
3. Run the below command to install the required packages:-
  - `pip install -r requirements.txt`
4. Move to project directory using below command:-
  - `cd fastapi`

# Database Setup and Installation.
1. Download and Install PostgreSQL in your computer using this link `https://www.postgresql.org/download/`.
2. Create a database.

# Setup environment variables.
Create a .env file and store your database credentials in below format:-
  - `dbname = 'name_of_db'`
  - `user= 'username_of_db'`
  - `password= 'password_of_db'`
  - `host= 'host_of_db'`
  - `port' =  'port_no_of_db'`
  - `MAIN_DATABASE_URL = 'url_of_main_db'`

# Run project.
1. Run the below command to load the data and run the project:-
  - `uvicorn main:app --reload`

# To access the API endpoints:
  - `/api/weather/`  -- for weather records
  - `/api/weather/stats/`  -- for weather stats
  - `/docs` -- for swagger documentation

# Testing.
To run the testcases use this command:-
  - `pytest`
