**Steps to run the project**
1. Clone the git repository.
2. Create and activate a virtual environment using the below commands:-
  - `pip install virtualenv`
  - `python -m venv env`
  - `source env/bin/activate`
3. Run the below command to install the required packages:-
  - `pip install -r requirements.txt`
4. Create a .env file and store your database credentials in below format:-
  - `dbname = 'name_of_db'`
  - `user= 'username_of_db'`
  - `password= 'password_of_db'`
  - `host= 'host_of_db'`
  - `port' =  'port_no_of_db'`
  - `MAIN_DATABASE_URL = 'url_of_main_db'`
  - `TESTING_DATABASE_URL = 'url_of_testing_db'`
5. Use `data_script.py` and `stats_script.py` file to dump the database using below commands:-
  - `python data_script.py`
  - `python stats_script.py`
4. Run the below command to run the project:-
  - `uvicorn main:app --reload`
5. There are two endpoints in this project:-
  - `/api/weather/`
  - `/api/weather/stats/`
6. To run the testcases use this command:-
  - `pytest`
