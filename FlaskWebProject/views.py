"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, Response, request
from FlaskWebProject import app
import json
import pymysql


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
            'type': request.form['type'],
            'dest-california': request.form['dest-Cali'],
            'dest-caribbean': request.form['dest-Caribbean'],
            'dest-mid-atlantic': request.form['dest-Mid-Atlantic'],
            'dest-mountain-desert': request.form['dest-MountainDesert'],
            'dest-northeast': request.form['dest-northeast'],
            'dest-southwest': request.form['dest-southwest'],
            'area-los-angeles': request.form['area-LosAngeles'],
            'area-san-francisco': request.form['area-SanFrancisco'],
            'area-pr': request.form['area-pr'],
            'area-dr': request.form['area-dr'],
            'area-colombia': request.form['area-Colombia'],
            'area-other-caribbean': request.form['area-OtherCaribbean'],
            'area-washington-dc': request.form['area-WashingtonDC'],
            'area-southern': request.form['area-Southern'],
            'area-west-mountain': request.form['area-WestMountain'],
            'area-pacific-nw': request.form['area-PacificNW'],
            'area-alaska': request.form['area-Alaska'],
            'area-nyc': request.form['area-NYC'],
            'area-upstate-ny': request.form['area-UpstateNY'],
            'area-boston': request.form['area-Boston'],
            'area-midtwest': request.form['area-Midwest'],
            'area-neislands': request.form['area-NEIslands'],
            'area-pbi': request.form['area-pbi'],
            'area-mcd': request.form['area-mcd'],
            'area-gulf': request.form['area-gulf'],
            'area-texas': request.form['area-texas'],
            'area-fill': request.form['area-fill'],
            'age': request.form['age'],
            'hometown': request.form['hometown'],
            'relationship': request.form['relationship']}

    return request.form['end-date']
    # return Response(response='test',
    #                 status=200,
    #                 mimetype="application/json")
