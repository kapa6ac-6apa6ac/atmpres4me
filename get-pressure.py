# get-pressure.py

################=Import_Libs=###############################

import urllib.request, urllib.error, urllib.parse
import re
import datetime
import psycopg2
from psycopg2 import Error

################=Save_Map_as_Page=##########################

url = 'http://www.meteorb.ru/weather/interaktiv-map-meteodata-repbashkortostan'
response = urllib.request.urlopen(url)
webContent = response.read()

page = open('map', 'wb')
page.write(webContent)
page.close

################=Check_Date_and_Time=#######################

date = datetime.datetime.today().strftime("%d.%m.%Y")
time = datetime.datetime.today().strftime("%H:00")

################=Get_Pressure_Value_From_File_map=##########

fh = open('map')
for line in fh:
        if 'st37' in line:
            result = re.findall(r'\d{3}', line)
fh.close()

################=Change_Value_str_to_int=###################

result1 = [int(x) for x in result]

################=Connect_to_PGSQL=##########################

try:
    # Connecting to an existing database
    connection = psycopg2.connect(user="dbuser",
                                  # Password for PostgreSQL DB user
                                  password="**********",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="weather")

    cursor = connection.cursor()

################=Insert_Data_to_BD_weather=#################

    postgres_insert_query = """ INSERT INTO pressure (VALUE, TIME, DATE) VALUES (%s,%s,%s) """
    record_to_insert = ((result1[0]), time, date)
    cursor.execute(postgres_insert_query, record_to_insert)

    connection.commit()
    count = cursor.rowcount
    print(count, "Record inserted successfully into pressure table")

except (Exception, psycopg2.Error) as error:
    print("Failed to insert record into table,", error)

finally:
    # closing database connection.
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

################=End_of_Script=#############################
