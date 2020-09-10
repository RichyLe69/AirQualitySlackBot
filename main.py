import geocoder
import requests
import json
import os
from flask import Flask, Response
from slackeventsapi import SlackEventAdapter
from threading import Thread
from slack import WebClient

# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client

from utils import crypto_main

# This `app` represents your existing Flask app
app = Flask(__name__)

aqi_command = ['aqi']
aqi_threshold = 100

baseurl = "https://api.breezometer.com/air-quality/v2/current-conditions?lat={}&lon={}&key={}&features=breezometer_aqi,local_aqi,health_recommendations"
breezokey = ''
account_sid = ''
auth_token = ''

SLACK_SIGNING_SECRET = ''
slack_token = ''
VERIFICATION_TOKEN = ''

client = Client(account_sid, auth_token)

# instantiating slack client
slack_client = WebClient(slack_token)

# An example of one of your Flask app's routes
@app.route("/")
def event_hook(request):
    json_dict = json.loads(request.body.decode("utf-8"))
    if json_dict["token"] != VERIFICATION_TOKEN:
        return {"status": 403}

    if "type" in json_dict:
        if json_dict["type"] == "url_verification":
            response_dict = {"challenge": json_dict["challenge"]}
            return response_dict
    return {"status": 500}
    return


slack_events_adapter = SlackEventAdapter(
    SLACK_SIGNING_SECRET, "/slack/events", app
)


@slack_events_adapter.on("app_mention")
def handle_message(event_data):
    def send_reply(value):
        event_data = value
        message = event_data["event"]
        if message.get("subtype") is None:
            command = message.get("text")
            channel_id = message["channel"]
            # if any(item in command.lower() for item in aqi_command):
            if command.split('> ')[1].split(' ')[0] == 'aqi':
                my_zip = (command.split('aqi ')[1])
                query = breezometer_query(my_zip)
                message2 = '{}, AQI: {}. \n{}. \n{}'.format(query[0], query[1], query[2], query[3])
                slack_client.chat_postMessage(channel=channel_id, text=message2)
            if command.split('> ')[1].split(' ')[0] == 'crypto':
                print('crypto command')
                crypto_symbol = (command.split('crypto ')[1])
                response = crypto_main(crypto_symbol)
                message = 'The price for {} is {}'.format(response[0], response[1])
                slack_client.chat_postMessage(channel=channel_id, text=message)
            else:
                message = 'Unknown Command. Try "@airbot aqi <zipcode>"'
                slack_client.chat_postMessage(channel=channel_id, text=message)
    thread = Thread(target=send_reply, kwargs={"value": event_data})
    thread.start()
    return Response(status=200)


def get_lat_lon_loc(zipcode):
    g = geocoder.arcgis(zipcode)
    print(g.status)
    if g.status == "OK":
        lat = g.json.get("lat")
        lon = g.json.get("lng")
        loc = g.json.get('address')
        return lat, lon, loc


def get_air_quality(lat, lon):
    response = requests.get(baseurl.format(lat, lon, breezokey))
    if response.status_code == 200:
        json_data = json.loads(response.text)
        return json_data


def create_text_message(loc, aqi, category):
    # print('Location: {} - AQI: {}. {}.'.format(loc, aqi, category))
    message = client.messages \
        .create(
        body="Location: {} - AQI: {}. {}.".format(loc, aqi, category),
        from_='+',
        to='+'
    )
    print(message.sid)


def breezometer_query(zipcode):
    lat_lon_loc = get_lat_lon_loc(zipcode)
    breezometer_response = get_air_quality(lat_lon_loc[0], lat_lon_loc[1])
    aqi = breezometer_response['data']['indexes']['usa_epa']
    health_rec = breezometer_response['data']['health_recommendations']['general_population']
    if aqi['aqi'] > aqi_threshold:
        create_text_message(lat_lon_loc[2], aqi['aqi'], aqi['category'])
    return lat_lon_loc[2], aqi['aqi'], aqi['category'], health_rec


if __name__ == '__main__':
    app.run(port=3000)
