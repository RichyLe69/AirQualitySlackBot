# Air Quality Slack Bot

![Alpha status](https://img.shields.io/badge/Project%20status-Alpha-red.svg)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![PyPI pyversions](https://camo.githubusercontent.com/fd8c489427511a31795637b3168c0d06532f4483/68747470733a2f2f696d672e736869656c64732e696f2f707970692f707976657273696f6e732f77696b6970656469612d6170692e7376673f7374796c653d666c6174)](https://pypi.python.org/pypi/ansicolortags/)

Designed to retrieve air quality index and other information for slack users.

# Requirements

Python 3, Slack API, Breezometer API Key, Twilio API Key.

# Bot Uses

Retrieve live Air Quality Index (AQI) data from breezometer and posts it to configured slack channels. 

* Users can specify location by providing their desired zip code.

* If the AQI exceeds a particular threshold (unhealthy), a text message SMS notification from twilio will be sent to user's mobile phone.

* Information regarding the health condition of the air quality will be provided by Breezometer's Standards.

# Example 

![Alt Text]()
![Alt Text]()
![Alt Text]()
