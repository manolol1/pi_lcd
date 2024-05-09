from flask import Flask
import config
from threading import Thread

app = Flask(__name__)

@app.route('/')
def index():
    return "To control lcd backlight, use /backlight/on or /backlight/off."

@app.route('/backlight/on')
def backlight_on():
    setBacklight(True)
    return "Backlight on"

@app.route('/backlight/off')
def backlight_off():
    setBacklight(False)
    return "Backlight off"

def start_server(backlight_function):
    global setBacklight
    setBacklight = backlight_function
    flask_thread = Thread(target=app.run, kwargs={'host': '0.0.0.0', "port": config.getServerPort()})
    flask_thread.start()