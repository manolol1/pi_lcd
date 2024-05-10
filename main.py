import lcdlib.lcddriver as lcddriver
import weather
import server
from time import *
import datetime

lcd = lcddriver.lcd()

global backlight
backlight = 1

def setBacklight(state):
    global backlight

    if (state == "toggle"):
        match backlight:
            case 0:
                backlight = 1
                return 1
            case 1:
                backlight = 0
                return 0
    else:
        backlight = state

def autoBacklight():
    pass #TODO: Use light sensor

server.start_server(setBacklight)

while (True):
    dt = datetime.datetime.now()
    lcd.lcd_display_string(f"{dt.hour:02d}:{dt.minute:02d} - {dt.day:02d}.{dt.month:02d}.{dt.year:04d}", 1)
    lcd.lcd_display_string(str(weather.getCurrentTemperature()) + "ßC", 2)

    match backlight:
        case 0:
            lcd.lcd_backlight("off")
        case 1:
            lcd.lcd_backlight("on")
        case 2:
            autoBacklight()

    sleep(1)
