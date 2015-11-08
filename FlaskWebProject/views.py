"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, Response, request
from contextlib import closing
from FlaskWebProject import app
import json
import pymysql
from time import strftime


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )


@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )


@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )


@app.route('/submit', methods=['POST'])
def submit():
    # return 'Server successfully received data'
    info = {'start-date': request.form['start-date'],
            'end-date': request.form['end-date'],
            'type': request.form.getlist('type'),
            'max-budget': request.form['max-budget'],
            'dest-california': request.form['dest-California'],
            'dest-caribbean': request.form['dest-Caribbean'],
            'dest-mid-atlantic': request.form['dest-Mid-Atlantic'],
            'dest-mountain-desert': request.form['dest-MountainDesert'],
            'dest-northeast': request.form['dest-Northeast'],
            'dest-southwest': request.form['dest-Southwest'],
            # 'area-los-angeles': request.form['area-LosAngeles'],
            # 'area-san-francisco': request.form['area-SanFrancisco'],
            # 'area-pr': request.form['area-pr'],
            # 'area-dr': request.form['area-dr'],
            # 'area-colombia': request.form['area-Colombia'],
            # 'area-other-caribbean': request.form['area-OtherCaribbean'],
            # 'area-washington-dc': request.form['area-WashingtonDC'],
            # 'area-southern': request.form['area-Southern'],
            # 'area-west-mountain': request.form['area-WestMountain'],
            # 'area-pacific-nw': request.form['area-PacificNW'],
            # 'area-alaska': request.form['area-Alaska'],
            # 'area-nyc': request.form['area-NYC'],
            # 'area-upstate-ny': request.form['area-UpstateNY'],
            # 'area-boston': request.form['area-Boston'],
            # 'area-midwest': request.form['area-Midwest'],
            # 'area-neislands': request.form['area-NEIslands'],
            # 'area-pbi': request.form['area-pbi'],
            # 'area-mcd': request.form['area-mcd'],
            # 'area-gulf': request.form['area-gulf'],
            # 'area-texas': request.form['area-texas'],
            # 'area-fill': request.form['area-fll'],
            # 'age': request.form['age'],
            # 'hometown': request.form['hometown'],
            # 'relationship': request.form['relationship']
            }

    hostname = 'serv.byang.io'
    port = 3306
    username = 'root'
    password = 'cse305'
    dbName = 'thenorthstar'

    #
    #  hostname = 'us-cdbr-azure-east-a.cloudapp.net'
    # port = 3306
    # username = 'b67312773cea3d'
    # password = 'cf62f138'
    # dbName = 'thenorthstar'


    conn = pymysql.connect(host = hostname, port = port, user = username, passwd=password, db=dbName)

    type_string = ''
    for item in info['type']:
        type_string += 'city_pair_desttype.destination_type = ' + item + ' OR '
    type_string = type_string[:len(type_string)-3]


    with closing(conn.cursor()) as cur:
        sql = "SELECT DISTINCT city_pair_desttype.destination FROM city_pair_desttype WHERE city_pair_desttype.origin = 'JFK' AND (" + type_string + " )"
        cur.execute(sql)
        conn.commit()

        results = []



        destinations = ''
        for i in cur.fetchall():
            itemWeWant = i[0]
            destinations += "destination = \'" + itemWeWant + "\' OR "
        destinations = destinations[:len(destinations) - 3]


        sql = "SELECT DISTINCT origin, destination, flight_time, flight_date, dollar_fare FROM fare WHERE flight_date > \'" + info['start-date']
        sql += "\' AND flight_date < \'" + info['end-date']
        sql += "\' AND (" + destinations + ") AND origin=\'JFK\' AND dollar_fare <= " + info['max-budget'] + " ORDER BY flight_date ASC, dollar_fare ASC"
        print (sql)
        cur.execute(sql)
        conn.commit()

        destinations2 = ''
        for i2 in cur.fetchall():
            newArray = []
            for thingy in i2:
                newArray.append(str(thingy))
            results.append(newArray)
            itemWeWant = i2[1]
            destinations2 += "code = \'" + itemWeWant + "\' OR "
        destinations2 = destinations2[:len(destinations2) - 3]

        sql = "SELECT DISTINCT code, latitude, longitude, city FROM airport_locations WHERE (" + destinations2 + ")"
        cur.execute(sql)
        conn.commit()
        locationMap = []
        for thing in cur.fetchall():
            locationMap.append(thing)

        thing2= {'result': results,
                'locationMap': locationMap
                }

        return Response(response=json.dumps(thing2),
                        status=200,
                        mimetype="application/json")


    #
    #
    # return Response(response=json.dumps(info),
    #                 status=200,
    #                 mimetype="application/json")
