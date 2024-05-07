from time import *
import requests
import threading
import config

global weatherKey, apiEndpoint, weatherData, weatherCity
weatherKey = config.getWeatherApiKey()
apiEndpoint = "https://api.openweathermap.org/data/2.5/weather"
weatherData = {"main": {"temp": 0}, "weather": [{"description": "e"}]} # temporary data to avoid crashes due to unset values
weatherCity = config.getWeatherLocation()

refreshInterval = 300

def weatherLoop():
    global weatherData

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

        print("Next weather data refresh in " + str(refreshInterval) + " seconds...")
        sleep(refreshInterval)

def getCurrentWeather():
    global weatherData
    return weatherData

def getCurrentTemperature():
    global weatherData
    return weatherData['main']['temp']

weatherThread = threading.Thread(target=weatherLoop) # start data refreshing loop in a separate thread
weatherThread.start()