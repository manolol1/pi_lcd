from flask import Flask
import config
from threading import Thread

app = Flask(__name__)

@app.route('/')
@app.route('/backlight')
def index():
    return "To control lcd backlight, use /backlight/on or /backlight/off.<br>Toggle with /backlight/toggle."

@app.route('/backlight/on')
def backlight_on():
    setBacklight(1)
    return "Backlight: on"

@app.route('/backlight/off')
def backlight_off():
    setBacklight(0)
    return "Backlight: off"

@app.route('/backlight/auto')
def backlight_auto():
    setBacklight(2)
    return "Backlight: auto"

@app.route('/backlight/toggle')
def backlight_toggle():
    state = setBacklight("toggle")
    return "Backlight toggled (now " + state + ")"


def start_server(backlight_function):
    global setBacklight
    setBacklight = backlight_function
    flask_thread = Thread(target=app.run, kwargs={'host': '0.0.0.0', "port": config.getServerPort()})
    flask_thread.start()