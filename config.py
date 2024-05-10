import configparser
import os
import sys
import requests

config = configparser.ConfigParser()

# generate default config, if no config file exists
if not os.path.exists('config.ini'):
    print("No config file found. Generating default config...")
    config['Weather'] = {'ApiKey': 'insert your openweathermap.org api key here',
                         'Location': 'Linz',}
    
    config['WebServer'] = {'Enabled': 'False',
                           'Port': '5000'}
    
    config['Button'] = {'Enabled': 'False',
                        'Pin': '26'}

    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    print("Default config file generated. Please edit config.ini and restart the program.")
    sys.exit(1)

config.read('config.ini')

def testWeatherApi():
    params = {"q": getWeatherLocation(), "units": "metric", "appid": getWeatherApiKey(), "lang": "de"}
    try:
        request = requests.get(url = "https://api.openweathermap.org/data/2.5/weather", params = params)
        return request.status_code == 200
    except:
        return False

# read config file and create methods for getting the values
try:
    config.read('config.ini')

    def getWeatherApiKey():
        return config['Weather']['ApiKey']

    def getWeatherLocation():
        return config['Weather']['Location']

    def getServerEnabled():
        return config['WebServer']['Enabled'].lower()

    def getServerPort():
        return config['WebServer']['Port']
    
    def getButtonEnabled():
        return config['Button']['ButtonEnabled'].lower()
    
    def getButtonPin():
        return config['Button']['Pin']
except:
    print("An error occured while reading or writing the config file")