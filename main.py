import lcdlib.lcddriver as lcddriver
import weather
from time import *
import datetime
import config

weather.startWeatherThread()

lcd = lcddriver.lcd()

global backlight
backlight = 1

def setBacklight(state):
    global backlight

    if (state == "toggle"):
        if (config.getLightSensorEnabled() == "false"):
            match backlight:
                case 0:
                    backlight = 1
                    return "on"
                case 1:
                    backlight = 0
                    return "off"
        else:
            match backlight:
                case 0:
                    backlight = 1
                    return "on"
                case 1:
                    backlight = 2
                    return "auto"
                case 2:
                    backlight = 0
                    return "off"
    else:
        backlight = state

def autoBacklight():
    pass #TODO: Use light sensor

if (config.getServerEnabled() == "true"):
    import server
    server.start_server(setBacklight)

if (config.getButtonEnabled() == "true"):
    from gpiozero import Button # type: ignore

    try:
        button_pin = int(config.getButtonPin())
        button = Button(button_pin)
    except ValueError:
        print(f"Invalid pin number: {config.getButtonPin()}")
    except RuntimeError as e:
        print(f"Failed to initialize button on pin {button_pin}: {str(e)}")
        
    button.when_pressed = lambda: setBacklight("toggle")

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
