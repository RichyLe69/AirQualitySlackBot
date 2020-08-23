import geocoder
import requests
import json
import os

# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


baseurl = "https://api.breezometer.com/air-quality/v2/current-conditions?lat={}&lon={}&key={}&features=breezometer_aqi,local_aqi,health_recommendations"
breezokey = ''
account_sid = ''
auth_token = ''

client = Client(account_sid, auth_token)


def get_lat_lon_loc(zipcode):
    g = geocoder.arcgis(zipcode)
    print(g.status)
    if g.status == "OK":
        lat = g.json.get("lat")
        lon = g.json.get("lng")
        loc = g.json.get('address')
        # print(lat)
        # print(lon)
        # print(loc)
        return lat, lon, loc


def get_air_quality(lat, lon):
    # print('hello {} {}'.format(lat, lon))
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

# refine this to be only texting, not searching lat,lon, aqi. not needed for sending sms
def send_aqi_alert_sms(zipcode):
    lat_lon_loc = get_lat_lon_loc(zipcode)
    breezometer_response = get_air_quality(lat_lon_loc[0], lat_lon_loc[1])
    # breezometer_response['data']
    datetime = breezometer_response['data']['datetime']
    aqi = breezometer_response['data']['indexes']['usa_epa']
    # health_rec = breezometer_response['data']['health_recommendations']
    # print(datetime)
    # print(health_rec)
    create_text_message(lat_lon_loc[2], aqi['aqi'], aqi['category'])


if __name__ == '__main__':
    send_aqi_alert_sms(95118)
