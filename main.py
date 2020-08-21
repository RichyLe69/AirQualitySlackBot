# from flask import Flask, request, abort
import geocoder
import requests
import json
import os

# app = Flask(__name__)

baseurl = "https://api.ambeedata.com/latest/by-lat-lng"

def get_avg_AQI(aqis):
    sum = 0
    # for data in aqis["data"]:
    #     sum = sum + int(data["AQI"])
    print(aqis['stations']["AQI"])
    # avg = aqis['stations']["AQI"]
    return int(0)

def get_air_quality(zipcode):
    '''
    Get the location data (as zipcode or free form). Use geocoder to lookup from google
    convert it to lat/lon and feed it to Breezometer API to get the AQI and some more data.
    :param zipcode:
    :return:
    '''
    # token = os.environ["AMBEE_TOKEN"]
    token = "RCFe33UFMMaGtr6tIX3FU6JcAQugZHjfa9jgsJKf"

    air_quality = {}
    g = geocoder.arcgis(zipcode)
    print (g.status)
    if g.status == "OK":
        lat = g.json.get("lat")
        lon = g.json.get("lng")
        print(lat)
        print(lon)
        url = "{}/?lat={}&lng={}".format(baseurl, lat, lon)
        print(url)
        headers = {"accept": "application/json", "x-api-key": token}
        try:
            r = requests.get(url, headers=headers)

            if r.json()['message'] == "Success":
                print(r.json())
                air_quality["status"] = "OK"
                air_quality["aqi"] = get_avg_AQI(r.json())
                air_quality["location"] = r.json()["data"][0]["division"]
                air_quality["message"] = "Air quality in {} is: {}".format(air_quality["location"], air_quality["aqi"])
                print('successful if statement')
            elif r.json()["message"] != "success":
                print(r.json())
                print('message is not success, exiting')
                exit(0)
        except requests.exceptions.RequestException as e:
            air_quality["status"] = "ERROR"
            air_quality["message"] = "{}".format(e)
            print('except statement')
    else:
        air_quality["status"] = "ERROR"
        air_quality["message"] = "Location Unknown!"
        print('not ok')
    return air_quality


# @app.route('/')
# def api_root():
#     return "Oh hai! This is an API endpoint and this is not the URL you're looking for :)"


# @app.route("/aqi-slack", methods=['POST'])
# def slackpost():
#     '''
#     Creates a slack slash command endpoint. No token needed.
#     :return:
#     '''
#     token = request.form.get('token', None)
#     command = request.form.get('command', None)
#     zipcode = request.form.get('text', None)
#     returned = {}
#     message = get_air_quality(zipcode)
#     if message["status"] == "OK":
#         aqi = message["aqi"]
#         color = "green"
#     else:
#         message["message"] = "This location is not recognized"
#         color = "red"
#
#     return message["message"]


# @app.route("/aqig/<zipcode>", methods=["GET"])
# def aqig(zipcode):
#     '''
#     Creates a GET api endpoint where we can query this feeding the parameter at the end of the URL
#     Example: http://127.0.0.1:8000/aqig/Istanbul
#     :param zipcode:
#     :return:
#     '''
#     returned = {}
#     message = get_air_quality(zipcode)
#     if message["status"] == "OK":
#         aqi = message["aqi"]
#         color = "green"
#     else:
#         message["message"] = "This location is not recognized"
#         color = "red"
#         print ("Something wrong with the request... aborting")
#         abort(405)
#     returned["color"] = color
#     returned["message"] = message["message"]
#     returned["notify"] = False
#     returned["message_format"] = "text"
#     returned["aqi"] = int(aqi)
#     returned_json = json.dumps(returned)
#     return returned_json

if __name__ == '__main__':
    # if os.environ.get('AIR_PORT'):
    #     port = os.environ.get('AIR_PORT')
    # else:
    #     port = "5000"
    # if os.environ.get('AIR_IP'):
    #     ip = os.environ.get('AIR_IP')
    # else:
    #     ip = "127.0.0.1"
    # if os.environ.get('DEBUG'):
    #     debug = True
    # else:
    #     debug = False
    # app.run(host=ip, debug=debug, port=port)
    message = get_air_quality(95118)
    print('out of function')
    print(message)
    if message["status"] == "OK":
        aqi = message["aqi"]
        color = "green"
        print (message["message"])
    else:
        message["message"] = "This location is not recognized"
        color = "red"
        print(message["message"])
