import os
import logging
import psycopg2
from dotenv import load_dotenv

try:
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename='script.log'
    )

    load_dotenv()
    db_params = {
        'dbname': os.getenv("dbname"),
        'user': os.getenv("user"),
        'password': os.getenv("password"),
        'host': os.getenv("host"),
        'port': os.getenv("port")
    }
    insert_into_stats_query = '''
        INSERT INTO STATS (avg_max_temperature, avg_min_temperature, avg_precipitation, station_id, year)
        SELECT
            AVG(max_temperature / 10) AS avg_max_temperature,
            AVG(min_temperature / 10) AS avg_min_temperature,
            AVG(precipitation / 10) AS avg_precipitation,
            station_id,
            date_part('year', date) as year
        FROM
            record
        WHERE
            max_temperature IS NOT NULL
            AND min_temperature IS NOT NULL
            AND precipitation IS NOT NULL
        GROUP BY
            year, station_id;
         '''

    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()
    cursor.execute(insert_into_stats_query)
    connection.commit()
    cursor.close()
    connection.close()
except Exception as e:
    print(e)
    logging.error(str(e))
