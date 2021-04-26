import psycopg2
import json
import requests
import flask
from flask import request
from itertools import chain
import databaseconfig
from flask_cors import CORS
import jsonify
import coviddata
# import newsfeed
import random

app = flask.Flask(__name__)
app.config["DEBUG"] = True
cors = CORS(app)

@app.route('/getHospitals', methods=['GET'])
def getHospitals():
    
    url = "https://api.rootnet.in/covid19-in/hospitals/medical-colleges"
    payload = ""
    headers = {}
    response = requests.request("GET", url, data=payload, headers=headers)
    result = response.text

    hospitals = json.loads(result)["data"]["medicalColleges"]

    finalresponse = []
    for i in range(len(hospitals)):
        finalresponse.append({
            "hospitalid": i+1,
            "hospitalname": hospitals[i]['name'],
        })

    return json.dumps({"data":finalresponse})
   

@app.route('/getHospitalById', methods=['GET'])
def getHospitalById():
    
    url = "https://api.rootnet.in/covid19-in/hospitals/medical-colleges"
    payload = ""
    headers = {}
    response = requests.request("GET", url, data=payload, headers=headers)
    result = response.text

    hospitals = json.loads(result)["data"]["medicalColleges"]
    hospitalid = request.args['hospitalid']
    
    finalresponse = []
    for i in range(len(hospitals)):
        if (i+1) == int(hospitalid):
            locationdetails = getLocation(hospitals[i]['name'])
            finalresponse.append({
                "hospitalid": hospitalid,
                "hospitalname": hospitals[i]['name'],
                "hospitaladd": locationdetails['hospitaladd'],
                "hospitallon": locationdetails['hospitallong'],
                "hospitallat": locationdetails['hospitallat'],
                "hospitalcapacity": hospitals[i]['admissionCapacity'],
                "bedsavailable": hospitals[i]['hospitalBeds'],
                "contactpersonnumber": random.randint(9987623901, 9999026719)
            })

    return json.dumps({"data":finalresponse})


@app.route('/getStates', methods=['GET'])
def getState():
    
    url = "https://api.rootnet.in/covid19-in/hospitals/beds"

    payload = ""
    headers = {}
    response = requests.request("GET", url, data=payload, headers=headers)
    result = response.text

    states = json.loads(result)["data"]["regional"]

    finalresponse = []
    for i in range(len(states)):
        finalresponse.append({
            "stateid": i+1,
            "statename": states[i]['state'],
        })

    return json.dumps({"data":finalresponse})

@app.route('/getCities', methods=['GET'])
def getCities():
    url = "https://api.rootnet.in/covid19-in/hospitals/medical-colleges"
    payload = ""
    headers = {}
    response = requests.request("GET", url, data=payload, headers=headers)
    result = response.text

    hospitals = json.loads(result)["data"]["medicalColleges"]
    hospitalstate = request.args['hospitalstate']

    finalresponse = []
    for i in range(len(hospitals)):
        if hospitals[i]['state'] == hospitalstate:
            finalresponse.append({
                "cityid": i+1,
                "cityname": hospitals[i]['city']
            })

    return json.dumps({"data":finalresponse})


@app.route('/getHospitalByState', methods=['GET'])
def getHospitalByState():
    url = "https://api.rootnet.in/covid19-in/hospitals/medical-colleges"
    payload = ""
    headers = {}
    response = requests.request("GET", url, data=payload, headers=headers)
    result = response.text

    hospitals = json.loads(result)["data"]["medicalColleges"]
    hospitalstate = request.args['hospitalstate']
    
    finalresponse = []
    for i in range(len(hospitals)):
        if hospitals[i]["state"] == hospitalstate:
            finalresponse.append({
                "hospitalid": i+1,
                "hospitalname": hospitals[i]['name'],
            })

    return json.dumps({"data":finalresponse})
    

@app.route('/getHospitalByCity', methods=['GET'])
def getHospitalByCity():
    url = "https://api.rootnet.in/covid19-in/hospitals/medical-colleges"
    payload = ""
    headers = {}
    response = requests.request("GET", url, data=payload, headers=headers)
    result = response.text

    hospitals = json.loads(result)["data"]["medicalColleges"]
    hospitalcity = request.args['hospitalcity']

    finalresponse = []
    for i in range(len(hospitals)):
        if hospitals[i]["city"] == hospitalcity:
            finalresponse.append({
                "hospitalid": i+1,
                "hospitalname": hospitals[i]['name'],
            })

    return json.dumps({"data":finalresponse})

    
@app.route('/getStateWiseCovidData', methods=['GET'])
def getStateWiseCovidData():
    
    state = request.args['state']
    data = coviddata.statewisedata(state)
   
    return data

@app.route('/getBedsDetails', methods=['GET'])
def getBedsDetails():
    
    payload = ""
    headers = {}
    result = ""
    bedsvacant = 0

    filterby = request.args['filterby']
    value = request.args['value']

    if filterby == 'all':
        url = "https://api.rootnet.in/covid19-in/hospitals/beds"
        response = requests.request("GET", url, data=payload, headers=headers)
        result = response.text
        bedsvacant = json.loads(result)["data"]["summary"]["totalBeds"]
        
    elif filterby == 'state':
        url = "https://api.rootnet.in/covid19-in/hospitals/beds"
        response = requests.request("GET", url, data=payload, headers=headers)
        result = response.text
        allbedsvacant = json.loads(result)["data"]["regional"]
        for i in range(len(allbedsvacant)):
            if allbedsvacant[i]["state"] == value:
                bedsvacant = bedsvacant + allbedsvacant[i]["totalBeds"]

    elif filterby == 'city':
        url = "https://api.rootnet.in/covid19-in/hospitals/medical-colleges"
        response = requests.request("GET", url, data=payload, headers=headers)
        result = response.text
        allbedsvacant = json.loads(result)["data"]["medicalColleges"]
        for i in range(len(allbedsvacant)):
            if allbedsvacant[i]["city"] == value:
                bedsvacant = bedsvacant + allbedsvacant[i]["hospitalBeds"]
    

    finalresponse = {"BedsVacant": str(bedsvacant)}
    
    return finalresponse


@app.route('/getAllSurvivors', methods=['GET'])
def getAllSurvivors():
    conn = psycopg2.connect(
        database = databaseconfig.database, 
        user = databaseconfig.user, 
        password = databaseconfig.password, 
        host = databaseconfig.host, 
        port = databaseconfig.port
    )
    cursor = conn.cursor()
    cursor.execute("select version()")
    data = cursor.fetchone()
    print("Connection established to: ",data)
    cursor = conn.cursor()

    cursor.execute('''SELECT row_to_json(survivors) from survivors''')
    result = cursor.fetchall()
    result = list(chain.from_iterable(result))

    # return str(result)
    return json.dumps({"data":result})

@app.route('/getSurvivorById', methods=['GET'])
def getSurvivorById():
    conn = psycopg2.connect(
        database = databaseconfig.database, 
        user = databaseconfig.user, 
        password = databaseconfig.password, 
        host = databaseconfig.host, 
        port = databaseconfig.port
    )
    cursor = conn.cursor()
    cursor.execute("select version()")
    data = cursor.fetchone()
    print("Connection established to: ",data)
    cursor = conn.cursor()

    survivorid = request.args['survivorid']

    cursor.execute('''SELECT row_to_json(survivors) from survivors where survivorid='''+ survivorid +''' ''')
    result = cursor.fetchall()
    result = list(chain.from_iterable(result))

    # return str(result)
    return json.dumps({"data":result})

@app.route('/getNewsFeed', methods=['GET'])
def getNewsFeed():
    url = "http://news.google.com/news?q=covid-19&hl=en-US&sort=date&gl=US&num=100&output=rss"
    feed = newsfeed.ParseFeed(url)
    finalresponse = feed.parse()
    print(finalresponse)
    return finalresponse


@app.route('/getLatitudeLongitude', methods=['GET'])
def getLatitudeLongitude():
    from geopy.geocoders import Nominatim

    place = request.args['place']
    try:
        geolocator = Nominatim(user_agent="Your_Name")
        location = geolocator.geocode(place)
        
        return {"placelat": location.latitude, "placelon": location.longitude}
    except:
        place = place.split(',')
        place = place[len(place)-1]
        try:
            geolocator = Nominatim(user_agent="Your_Name")
            location = geolocator.geocode(place)
        
            return {"placelat": location.latitude, "placelon": location.longitude}
        except:
            return {"placelat": 16.67613485, "placelon": 81.17086824015968}


def getLocation(address):
    from geopy.geocoders import Nominatim
    # address='Nagpur'
    # address='Tezpur Medical College & Hospital, Tezpur'
    # address='RVS Institute of Medical Sciences, Chittoor'
    try:
        geolocator = Nominatim(user_agent="Your_Name")
        location = geolocator.geocode(address)
        
        return {"hospitallat": location.latitude, "hospitallong": location.longitude, "hospitaladd": location.address}
    except:
        address = address.split(',')
        address = address[len(address)-1]
        try:
            geolocator = Nominatim(user_agent="Your_Name")
            location = geolocator.geocode(address)
        
            return {"hospitallat": location.latitude, "hospitallong": location.longitude, "hospitaladd": location.address}
        except:
            return {"hospitallat": 16.67613485, "hospitallong": 81.17086824015968, "hospitaladd": "NA"}

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
