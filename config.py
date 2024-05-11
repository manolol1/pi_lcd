import configparser
import os
import sys
import requests

config = configparser.ConfigParser()

# generate default config, if no config file exists
if not os.path.exists('config.ini'):
    print("No config file found. Generating default config...")
    
    config['general'] = {'default_backlight': '1',
                         'lcd_lines': '4',
                         'lcd_columns': '20'
                         }

    config['weather'] = {'api_key': 'insert your openweathermap.org api key here',
                         'location': 'linz',
                         'refresh_interval': '300'
                         }
    
    config['webserver'] = {'enabled': 'false',
                           'port': '5000'}
    
    config['button'] = {'enabled': 'false',
                        'pin': '0'}
    
    config['lightsensor'] = {'enabled': 'false',
                             'pin': '0'}

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

    def getDefaultBacklight():
        return int(config['general']['default_backlight'])

    def getLcdLines():
        return int(config['general']['lcd_lines'])

    def getLcdColumns():
        return int(config['general']['lcd_columns'])

    def getWeatherApiKey():
        return config['weather']['api_key']

    def getWeatherLocation():
        return config['weather']['location']
    
    def getWeatherRefreshInterval():
        return int(config['weather']['refresh_interval'])

    def getServerEnabled():
        return config['webserver']['enabled'].lower()

    def getServerPort():
        return config['webserver']['port']
    
    def getButtonEnabled():
        return config['button']['enabled'].lower()
    
    def getButtonPin():
        return config['button']['pin']
    
    def getLightSensorEnabled():
        return config['lightsensor']['enabled'].lower()
    
    def getLightSensorPin():
        return config['lightsensor']['pin']
except:
    print("An error occured while reading or writing the config file")