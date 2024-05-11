import lcdlib.lcddriver as lcddriver
import weather
from time import *
import datetime
import config
import threading

weather.startWeatherThread()

lcd = lcddriver.lcd()

global backlight
backlight = 1

def setBacklight(state):
    global backlight, notification

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
                    notification("Backlight mode: auto")
                    return "auto"
                case 2:
                    backlight = 0
                    return "off"
    elif (state == 2):
        backlight = 2
        notification("Backlight mode: auto")
        return "auto"
    else:
        backlight = int(state)
        return state
    

if (config.getServerEnabled() == "true"):
    import server
    server.start_server(setBacklight)

if (config.getButtonEnabled() == "true"):
    from gpiozero import Button # type: ignore

    try:
        button_pin = int(config.getButtonPin())
        button = Button(button_pin)
    except ValueError:
        print(f"Invalid button pin number: {config.getButtonPin()}")
    except RuntimeError as e:
        print(f"Failed to initialize button on pin {button_pin}: {str(e)}")
        
    button.when_pressed = lambda: setBacklight("toggle")


if (config.getLightSensorEnabled() == "true"):
    from gpiozero import DigitalInputDevice # type: ignore

    try:
        lightSensor_pin = int(config.getLightSensorPin())
        lightSensor = DigitalInputDevice(lightSensor_pin)
    except ValueError:
        print(f"Invalid light sensor pin number: {config.getLightSensorPin()}")
    except RuntimeError as e:
        print(f"Failed to initialize light sensor on pin {lightSensor_pin}: {str(e)}")
    
    backlight = 2

def autoBacklight():
    global lightSensor

    if (lightSensor.value == 0):
        lcd.lcd_backlight("on")
    else:
        lcd.lcd_backlight("off")

def notificationLoop(message):
    global backlight
    temp = backlight
    
    lcd.lcd_display_string(message, 4)

    timeLeft = 5
    while (timeLeft > 0):
        backlight = 1
        sleep(1)
        timeLeft -= 1
    
    backlight = temp
    lcd.lcd_clear()

def notification(message):
    notificationThread = threading.Thread(target=notificationLoop, args=(message,))
    notificationThread.start()

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
