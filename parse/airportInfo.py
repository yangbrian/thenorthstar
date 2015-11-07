__author__ = 'Brian'

from contextlib import closing
from bs4 import BeautifulSoup as soup, Tag
from string import ascii_uppercase
import pymysql
import requests, time
import wikipedia

# Pull all unique airport codes from the dataset we got
def get_unique_airport_codes(cursor, connection):
    # get all unique origin airports
    sql_origin = "SELECT DISTINCT origin FROM fare"
    cursor.execute(sql_origin)
    origin_list = cursor.fetchall()

    # get all unique destination airports
    sql_dest = "SELECT DISTINCT destination FROM fare"
    cursor.execute(sql_dest)
    dest_list = cursor.fetchall()

    # merge the two so we only have unique values
    merged_list = list(set(origin_list + dest_list))
    # print(merged_list)

    # add to database
    new_list = []
    for item in merged_list:
        airport_code = item[0].strip()
        new_list.append(airport_code)
        sql = "INSERT INTO airport_locations(code) VALUES (%s)"

        # cursor.execute(sql, airport_code)
        # connection.commit()

    # return the merged list
    return new_list

# scrape wikipedia. if we got the airport code, fill up the table with sweet sweet data
def scrape_wikipedia(unique_codes, cursor, connection):
    base_url = 'https://en.wikipedia.org/wiki/List_of_airports_by_IATA_code:_'
    base_wiki = 'https://en.wikipedia.org'

    # go through each page on wikipedia, letter by letter (26 letters)
    for c in ascii_uppercase:
        r = requests.get(base_url + c)
        s = soup(r.text, 'html.parser')

        # check each td for code match
        for item in s.find_all("td"):
            text = item.text.strip().upper()
            for code in unique_codes:

                # td is a match with an airport kit. time to do things.
                if code == text:
                    row = item.parent.contents
                    name = row[5].text
                    location_link = row[5].contents[0]
                    city = row[7].text
                    coordinates = get_coordinates(base_wiki + location_link['href'])
                    latitude = coordinates['latitude']
                    longitude = coordinates['longitude']

                    # print(text + '___' + str(latitude) + ' ' + str(longitude))
                    # print('code: ' + text + ' name: ' + name + ' locLink: ' + base_wiki + location_link['href'])

                    sql = "UPDATE airport_locations " \
                            "SET name=%s, city=%s, latitude=%s, longitude=%s " \
                            "WHERE code = %s"
                    cursor.execute(sql, (name, city, latitude, longitude, text))
                    connection.commit()

# gets the coordinates (decimals, not degrees) of a location, passed in by wiki link
def get_coordinates(wiki_link):
    # go to the wiki page
    r = requests.get(wiki_link)
    s = soup(r.text, 'html.parser')

    coords_lat = str(s.select('span.latitude')[0].contents[0].encode('utf-8'))

    # i hate unicode. :<
    latitude_deg = {'degrees': find_between(coords_lat, 'b\'', '\\xc2\\xb0'),
                    'minutes': find_between(coords_lat, '\\xc2\\xb0', '\\xe2\\x80\\xb2'),
                    'seconds': find_between(coords_lat, '\\xe2\\x80\\xb2', '\\xe2\\x80\\xb3'),
                    'multiplier': 1 if (coords_lat[len(coords_lat) - 2] == "N") else -1
                    }
    # print('d: ' + latitude_deg['degrees'] + ' m: ' + latitude_deg['minutes'] + ' s: ' + latitude_deg['seconds'] + ' mult: ' + str(latitude_deg['multiplier']) + ' dec: ' + str(deg_to_dec(latitude_deg)))

    coords_long = str(s.select('span.longitude')[0].contents[0].encode('utf-8'))
    longitude_deg = {'degrees': find_between(coords_long, 'b\'', '\\xc2\\xb0'),
                     'minutes': find_between(coords_long, '\\xc2\\xb0', '\\xe2\\x80\\xb2'),
                     'seconds': find_between(coords_long, '\\xe2\\x80\\xb2', '\\xe2\\x80\\xb3'),
                     'multiplier': 1 if (coords_long[len(coords_lat) - 2] == "W") else -1
                     }
    # print('d: ' + longitude_deg['degrees'] + ' m: ' + longitude_deg['minutes'] + ' s: ' + longitude_deg['seconds'] + ' mult: ' + str(longitude_deg['multiplier']) + ' dec: ' + str(deg_to_dec(longitude_deg)))

    return {'latitude': str(deg_to_dec(latitude_deg)),
            'longitude': str(deg_to_dec(longitude_deg))
            }

def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last)
        return s[start:end]
    except ValueError:
        return ""

# convert from degrees (latitude/longitude coordinates) to decimal representation
# decimals = degrees + minutes/60 + seconds/3600
# will catch errors/make this bomb proof later
def deg_to_dec(coordinates):
    return round(((float(coordinates['degrees']) + (float(coordinates['minutes']) / 60) + (float(coordinates['seconds']) / 3600)) * -1), 5)

# hostname = 'us-cdbr-azure-east-a.cloudapp.net'
# port = 3306p
# username = 'b67312773cea3d'
# password = 'cf62f138'
# dbName = 'northstar'

hostname = 'localhost'
port = 3306
username = 'root'
password = ''
dbName = 'northstar'

# connect to sql server
conn = pymysql.connect(host = hostname, port = port, user = username, passwd=password, db=dbName)

with closing(conn.cursor()) as cur:
    unique_codes = get_unique_airport_codes(cur, conn)
    scrape_wikipedia(unique_codes, cur, conn)