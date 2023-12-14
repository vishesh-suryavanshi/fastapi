import os
import logging
import psycopg2
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

try:
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename='script.log'
    )
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

    start_time = datetime.now()
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()
    insert_into_station = "INSERT INTO station (name) VALUES (%s);"
    insert_into_record = "INSERT INTO record (date, max_temperature, min_temperature," \
                         " precipitation, station_id) VALUES (%s, %s, %s, %s, %s)"
    select_id_of_station = f'SELECT id from station where name=%s'

    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        unique_records = set()
        cnt = 0
        station_name = Path(file_path).stem
        cursor.execute(insert_into_station, (station_name,))
        cursor.execute(select_id_of_station, (station_name,))
        station = cursor.fetchone()
        station_id = station[0]
        with open(file_path, 'r') as file:
            for line in file:
                data = line.strip().split('\t')
                temp_line = []
                for idx, cell in enumerate(data):
                    if idx == 0:
                        temp_line.append(datetime.strptime(str(cell), '%Y%m%d').date())
                    else:
                        temp_line.append(None if int(cell.strip()) == -9999 else int(cell.strip()))
                temp_line.append(station_id)
                unique_records.add(tuple(temp_line))
                cnt += 1
        for record in unique_records:
            cursor.execute(insert_into_record, record)
        end_time = datetime.now()
        logging.info(f'Start time {start_time}, End time {end_time}, Total Records {cnt}, '
                     f'Inserted Records {len(unique_records)}')
    connection.commit()
    cursor.close()
    connection.close()
except Exception as e:
    print(e)
    logging.error(str(e))
