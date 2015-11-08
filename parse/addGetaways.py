__author__ = 'Brian'

from contextlib import closing
import pymysql
import csv

# you can tell this is when hackathon mode kicks in.
def populate_getaways_table(cursor, connection):
    file = open('../rawData/YHack-Getaways-packages.csv', 'r')
    file.readline()
    with file as line:
        reader = csv.reader(line)
        for data in reader:
            sql = "INSERT INTO getaways(origin, destination, hotel_property, hotel_nights_stay, checkin_date, checkout_date," \
                    "expedia_price, jetblue_price, percent_savings, month, advance_weeks, count)" \
                  "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            print(data)
            cursor.execute(sql, (data[0], data[1], data[2], data[3], get_correct_date_format(data[4]),
                                 get_correct_date_format(data[5]), data[6], data[7], data[8], data[9], data[10], data[11]))
            connection.commit()


def get_correct_date_format(incorrect_format):
    split = incorrect_format.split('/')
    if int(split[1]) < 10:
        split[1] = '0' + split[1]
    if int(split[2]) < 10:
        split[2] = '0' + split[2]
    return split[0] + '-' + split[1] + '-' + split[2]

# hostname = 'us-cdbr-azure-east-a.cloudapp.net'
# port = 3306
# username = 'b67312773cea3d'
# password = 'cf62f138'
# dbName = 'thenorthstar'

hostname = 'localhost'
port = 3306
username = 'root'
password = ''
dbName = 'northstar'

# connect to sql server
conn = pymysql.connect(host = hostname, port = port, user = username, passwd=password, db=dbName)

with closing(conn.cursor()) as cur:
    populate_getaways_table(cur, conn)