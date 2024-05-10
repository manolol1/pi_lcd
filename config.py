import configparser
import os

config = configparser.ConfigParser()

# generate default config, if no config file exists
if not os.path.exists('config.ini'):
    config['Weather'] = {'ApiKey': 'insert your openweathermap.org api key here',
                         'Location': 'Linz',}
    
    config['WebServer'] = {'Enabled': 'False',
                           'Port': '5000'}
    
    config['Button'] = {'Enabled': 'False',
                        'Pin': '26'}

    with open('config.ini', 'w') as configfile:
        config.write(configfile)

config.read('config.ini')

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