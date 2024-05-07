import configparser
import os

config = configparser.ConfigParser()

if not os.path.exists('config.ini'):
    config['Settings'] = {'WeatherApiKey': 'insert your key here',
                         'WeatherLocation': 'Linz',
                         'ServerPort': '5000'}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

config.read('config.ini')

try:
    config.read('config.ini')

    def getWeatherApiKey():
        return config['Settings']['WeatherApiKey']

    def getWeatherLocation():
        return config['Settings']['WeatherLocation']

    def getServerPort():
        return config['Settings']['ServerPort']
except:
    print("An error occured while reading or writing the config file")