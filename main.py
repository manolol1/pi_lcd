import lcdlib.lcddriver as lcddriver
import weather
from time import *
import datetime

lcd = lcddriver.lcd()

while (True):
    dt = datetime.datetime.now()
    
    lcd.lcd_display_string(f"{dt.hour:02d}" + ":" + f"{dt.minute:02d}" + " - " + f"{dt.day:02d}" + "." + f"{dt.month:02d}" + "." + f"{dt.year:04d}")
    lcd.lcd_display_string(str(weather.getCurrentTemperature()) + "ßC", 2)
    sleep(1)