import lcdlib.lcddriver as lcddriver
import weather
from time import *
import datetime

lcd = lcddriver.lcd()

while (True):
    dt = datetime.datetime.now()
    
    lcd.lcd_display_string(dt.time().strftime("%H:%M:%S") + " - " + dt.date, 1)
    lcd.lcd_display_string(str(weather.getCurrentTemperature()) + "ßC", 2)
    sleep(1)