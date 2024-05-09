import lcdlib.lcddriver as lcddriver
import weather
import server
from time import *
import datetime

lcd = lcddriver.lcd()

global backlight
backlight = True

def setBacklight(state):
    global backlight
    if (state == 0):
        backlight = False
    elif (state == 1):
        backlight = True
    elif (state == 2):
        backlight = not backlight

server.start_server(setBacklight)

while (True):
    dt = datetime.datetime.now()
    lcd.lcd_display_string(f"{dt.hour:02d}" + ":" + f"{dt.minute:02d}" + " - " + f"{dt.day:02d}" + "." + f"{dt.month:02d}" + "." + f"{dt.year:04d}", 1)
    lcd.lcd_display_string(str(weather.getCurrentTemperature()) + "ßC", 2)

    if (backlight):
        lcd.lcd_backlight("on")
    else:
        lcd.lcd_backlight("off")

    sleep(1)
