import requests
import sqlite3 as sql
from random import choice


API_KEY = "AIzaSyCAgU40OXQVFZ5azzF13WtS20OM8pGFCH4"
DATABASE = "app/database/markers.db"


def query_places(location=None):
    request_url = ("""
        https://maps.googleapis.com/maps/api/place/details/json
        ?placeid=ChIJN1t_tDeuEmsRUsoyG83frY4&
        fields=name,rating,formatted_phone_number,formatted_address&
        key="""+API_KEY)
    r = requests.get(request_url)
    return r.text


def place_search(lat, lng):
    request_url = (
        "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
        "location="+str(lat)+","+str(lng)+"&radius=1500&fields=name&"
        "key="+API_KEY)
    r = requests.get(request_url)
    return r.json()["results"]


def retrieve_details(place_id):
    request_url = (
        "https://maps.googleapis.com/maps/api/place/details/json?"
        "placeid="+str(place_id)+"&"
        "fields=formatted_address,formatted_phone_number,types&"
        "key="+API_KEY)
    r = requests.get(request_url)
    return r.json()["result"]


def query_database(lat=None, lng=None, place_id=None):
    markers = []
    if (lat and lng):
        command = "SELECT * FROM Markers WHERE lat = {} AND lng = {}".format(lat, lng)
    else:
        command = "SELECT * FROM Markers WHERE id = '{}'".format(place_id)
    with sql.connect(DATABASE) as connection:
        cur = connection.cursor()
        cur.execute(command)
        markers = cur.fetchall()
        cur.close()
    return markers[0:10]


def add_marker_to_database(marker, marker_type=None):
    chars = ['E', 'L', 'M']
    if (marker_type is None):
        marker_type = choice(chars)
    marker['name'] = marker['name'].replace("'", "\\")
    insert_command = "INSERT INTO Markers (formatted_address, formatted_phone, id, m_name, lat, lng, m_type) Values('{}', '{}', '{}', '{}', {}, {}, '{}')".format(
            marker['address'], marker['phone'], marker['place_id'], marker['name'],
            marker['lat'], marker['lng'], marker_type)
    with sql.connect(DATABASE) as connection:
        cur = connection.cursor()
        cur.execute(insert_command)
        connection.commit()
        cur.close()