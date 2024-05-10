from time import *
import requests
import threading
import config
import sys

global weatherKey, apiEndpoint, weatherData, weatherCity, firstLoad, refreshInterval
weatherKey = config.getWeatherApiKey()
apiEndpoint = "https://api.openweathermap.org/data/2.5/weather"
weatherData = {"main": {"temp": 0}, "weather": [{"description": "e"}]} # temporary data to avoid crashes due to unset values
weatherCity = config.getWeatherLocation()

refreshInterval = 300
firstLoad = True

def weatherLoop():
    global weatherData, firstLoad

    while (True):
        try:
            print("Refreshing weather data...")

            params = {"q": weatherCity, "units": "metric", "appid": weatherKey, "lang": "de"}
            response = requests.get(url = apiEndpoint, params = params)
            data = response.json()
            print("Weather data was refreshed.")

            weatherData = data # refresh data
        except:
            print("An error occured whilst updating weather data")

        
        if (firstLoad):
            # reload faster for the first time to avoid having no data when the request takes too long
            firstLoad = False
            print("Next weather data refresh in 20 seconds...")
            sleep(20)
        else:
            print("Next weather data refresh in " + str(refreshInterval) + " seconds...")
            sleep(refreshInterval)


def getCurrentWeather():
    global weatherData
    return weatherData

def getCurrentTemperature():
    global weatherData
    return weatherData["main"]["temp"]

def startWeatherThread():
    if (config.testWeatherApi() == False):
        print("Weather API test failed. Please check your weather key and location in config.ini!")
        sys.exit(1)
    
    weatherThread = threading.Thread(target=weatherLoop)
    weatherThread.start()
    print("Weather thread started.")
    return weatherThread