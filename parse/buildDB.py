__author__ = 'Brian'
from contextlib import closing
import pymysql
import csv

def add_airport_region(cursor, connection):
    file = open('../rawData/AirportRegion-stg.csv', 'r')
    file.readline()
    with file as line:
        reader = csv.reader(line)
        for data in reader:
            sql = "INSERT INTO airport_region(airport_code, geo_region_id) VALUES (%s, %s)"
            print(data)
            cursor.execute(sql, (data[0], data[1]))
            connection.commit()


def add_city_dest_type(cursor, connection):
    file = open('../rawData/CityPairDestinationType-stg.csv', 'r')
    file.readline()
    with file as line:
        reader = csv.reader(line)
        for data in reader:
            sql = "INSERT INTO city_pair_destType(origin, destination, destination_type) VALUES (%s, %s, %s)"
            print(data)
            cursor.execute(sql, (data[0], data[1], data[2]))
            connection.commit()


def add_dest_type(cursor, connection):
    file = open('../rawData/DestinationType-stg.csv', 'r')
    file.readline()
    with file as line:
        reader = csv.reader(line)
        for data in reader:
            sql = "INSERT INTO destination_type(type_id, type_name, display_order) VALUES(%s, %s, %s)"
            print(data)
            cursor.execute(sql, (data[0], data[1], data[2]))
            connection.commit()


def add_fare(cursor, connection):
    file = open('../rawData/Fares.Fare-stg.csv', 'r')
    file.readline()
    with file as line:
        reader = csv.reader(line)
        for data in reader:
            # date in format mm/dd/yyyy. need it in yyyy-mm-dd
            dateInfo = data[3].split()
            date = dateInfo[0]
            split = date.split('/')
            if int(split[0]) < 10:
                split[0] = '0' + split[0]
            if int(split[1]) < 10:
                split[1] = '0' + split[1]
            date = split[2] + '-' + split[0] + '-' + split[1]
            time = dateInfo[1]

            print(data)
            sql = "INSERT INTO fare" \
                  "(batch_number, origin, destination, flight_date, flight_time, flight_type, fare_type, dollar_fare, dollar_tax, points_fare, points_tax, is_Domestic, is_Private)" \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cur.execute(sql, (data[0], data[1], data[2], date, time, data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11]))
            connection.commit()


def add_geo_region(cursor, connection):
    file = open('../rawData/GeographicRegion-stg.csv', 'r')
    file.readline()
    with file as line:
        reader = csv.reader(line)
        for data in reader:
            print(data)
            sql = "INSERT INTO geographic_region(region_id, market_group_id, region_name) VALUES (%s, %s, %s)"
            cursor.execute(sql, (data[0], data[1], data[2]))
            connection.commit()


def add_mac(cursor, connection):
    file = open('../rawData/MAC-stg.csv', 'r')
    file.readline()
    with file as line:
        reader = csv.reader(line)
        for data in reader:
            print(data)
            sql = "INSERT INTO mac(code, is_supported) VALUES (%s, %s)"
            cursor.execute(sql, (data[0], data[1]))
            connection.commit()


def add_market_group(cursor, connection):
    file = open('../rawData/MarketGroup-stg.csv')
    file.readline()
    with file as line:
        reader = csv.reader(line)
        for data in reader:
            print(data)
            sql = "INSERT INTO market_group(group_id, group_name) VALUES (%s, %s)"
            cursor.execute(sql, (data[0], data[1]))
            connection.commit()


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

# fancy way to auto-close the connection
with closing(conn.cursor()) as cur:

    # # airport code to region ID - two columns. skip first line.
    # add_airport_region(cur, conn)
    #
    # # city-pair-destinationType
    # add_city_dest_type(cur, conn)
    #
    # #destination type
    # add_dest_type(cur, conn)
    #
    # #fares
    add_fare(cur, conn)
    #
    # #geographic region
    # add_geo_region(cur, conn)
    #
    # #mac
    # add_mac(cur, conn)
    #
    # #market group
    # add_market_group(cur, conn)
