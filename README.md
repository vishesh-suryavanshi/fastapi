# Weather API with fastAPI.
There are 3 endpoints in this project:-
  1. `/api/weather/`
  2. `/api/weather/stats/`
  3. `/docs`

# Project Setup and Installation.
1. Clone the git repository.
2. Create and activate a virtual environment using the below commands:-
```bash

  python -m venv env
  source env/bin/activate #(For Mac and Linux)
  env\Scripts\activate #(For Windows)

```


3. Run the below command to install the required packages:-
```bash 
  pip install -r requirements.txt
  ```
4. Move to project directory using below command:-
```bash
cd fastapi
```

# Database Setup and Installation.
1. Download and Install PostgreSQL in your computer using this link `https://www.postgresql.org/download/`.
2. Create a database using below command:-
```bash
CREATE DATABASE database_name;
```

# Setup environment variables.
Create a .env file and store your database credentials in below format:-
```bash
'dbname' = 'name_of_db'
'user' = 'username_of_db'
'password' = 'password_of_db'
'host' = 'host_of_db'
'port' =  'port_no_of_db'
'MAIN_DATABASE_URL' = 'url_of_main_db'
'TESTING_DATABASE_URL' = 'url_of_test_db'
 ```

# Run project.
1. Run the below command to load the data and run the project:-
```bash
uvicorn main:app --reload
```
<img src="https://i.ibb.co/fY4HL0q/test3.png" alt="" height="100" width="450"/>

#### This step will take few minutes as it will dump the data in the initial setup.

# To access the API endpoints:
```bash
/api/weather/  #for weather records
/api/weather/stats/  #for weather stats
/docs #for swagger documentation
```
# Testing.
To run the testcases use this command:-
```bash
pytest
```

### Screenshot of Testcase output.
<img src="https://i.ibb.co/2WKg2Ht/image.png" alt="" />

# Screenshots of Postman Collection

<img src="https://i.ibb.co/S5LBYKB/Screenshot-2023-12-27-at-8-11-24-PM.png" alt="weather image" /> 
<br><br>
<img src="https://i.ibb.co/zXgK91S/Screenshot-2023-12-27-at-8-12-39-PM.png" alt="weather/stats" />
<br><br>
<img src="https://i.ibb.co/KLqR9tc/Screenshot-2023-12-27-at-8-13-26-PM.png" alt="Swagger image" />