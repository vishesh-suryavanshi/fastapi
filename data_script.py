import os
import logging
import psycopg2
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv



def load_file_data():
    try:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='script.log'
        )

        start_time = datetime.now()

        folder_path = 'data/wx_data'
        file_list = os.listdir(folder_path)

        load_dotenv()
        db_params = {
            'dbname': os.getenv("dbname"),
            'user': os.getenv("user"),
            'password': os.getenv("password"),
            'host': os.getenv("host"),
            'port': os.getenv("port")
        }

        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()
        insert_into_station = "INSERT INTO station (name) VALUES (%s);"
        insert_into_record = "INSERT INTO record (date, max_temperature, min_temperature," \
                             " precipitation, station_id) VALUES (%s, %s, %s, %s, %s)"
        select_id_of_station = f'SELECT id from station where name=%s'

        for file_name in file_list:
            if file_name.endswith('.txt'):
                file_path = os.path.join(folder_path, file_name)
                all_records = []
                station_name = Path(file_path).stem
                cursor.execute(insert_into_station, (station_name,))
                cursor.execute(select_id_of_station, (station_name,))
                station = cursor.fetchone()
                station_id = station[0]
                with open(file_path, 'r') as file:
                    for line in file:
                        data = line.strip().split('\t')
                        if '-9999' in data:
                            continue
                        else:
                            temp_line = []
                            for idx, cell in enumerate(data):
                                if idx == 0:
                                    temp_line.append(datetime.strptime(str(cell), '%Y%m%d').date())
                                else:
                                    temp_line.append(int(cell.strip()))
                            temp_line.append(station_id)
                            all_records.append(temp_line)
                for record in all_records:
                    cursor.execute(insert_into_record, record)
                end_time = datetime.now()
                logging.info(f'Start time {start_time}, End time {end_time}, Inserted Records {len(all_records)}')
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print(str(e))
        logging.error(str(e))


def calculate_stats_data():
    try:
        load_dotenv()
        db_params = {
            'dbname': os.getenv("dbname"),
            'user': os.getenv("user"),
            'password': os.getenv("password"),
            'host': os.getenv("host"),
            'port': os.getenv("port")
        }
        insert_into_stats_query = '''
            INSERT INTO STATS (avg_max_temperature, avg_min_temperature, total_precipitation, station_id, year)
            SELECT
                AVG(max_temperature / 10) AS avg_max_temperature,
                AVG(min_temperature / 10) AS avg_min_temperature,
                SUM(precipitation / 100.0) AS total_precipitation,
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
        print(str(e))


