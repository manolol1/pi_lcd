import lcdlib.lcddriver as lcddriver
import weather
from time import *
import datetime
import config
import threading

weather.startWeatherThread()

lcd = lcddriver.lcd()
lcd_lock = threading.Lock()

global backlight
backlight = config.getDefaultBacklight()

global lineBlocked
lineBlocked = [False] * config.getLcdLines() # lines that are blocked won't be updated in the main loop.

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
        if (config.getLightSensorEnabled() == "false"):
            backlight = 1
            print("Light sensor is disabled. Auto backlight mode is not available.")
            notification("auto mode off" if config.getLcdColumns() < 20 else "auto mode disabled")
            return
        
        backlight = 2

        notification("Backlight: auto" if config.getLcdColumns() < 20 else "Backlight mode: auto")
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

notificationQueue = []

def notificationLoop():
    global backlight, lineBlocked, notificationQueue
    temp = backlight
    
    while (True):
        if (notificationQueue):
            message = notificationQueue.pop(0)
            with lcd_lock:
                lineBlocked[config.getLcdLines() - 1] = True
                lcd.lcd_display_string(message, config.getLcdLines()) # display message in last line

            timeLeft = 5
            while (timeLeft > 0):
                backlight = 1
                sleep(1)
                timeLeft -= 1
            
            backlight = temp
            
            with lcd_lock:
                lcd.lcd_clear()
            lineBlocked[config.getLcdLines() - 1] = False
        else:
            sleep(1)

notificationThread = threading.Thread(target=notificationLoop)
notificationThread.start()

def notification(message):
    if notificationQueue.count(message) < 2: # avoid notification spam (from eg. server/backlight/auto)
        notificationQueue.append(message)
    else:
        print(f"Notification \"{message}\" was blocked due to spamming.")

while (True):
    dt = datetime.datetime.now()

    with lcd_lock:
        if (not lineBlocked[0]):
            if (config.getLcdColumns() >= 18):
                lcd.lcd_display_string(f"{dt.hour:02d}:{dt.minute:02d} - {dt.day:02d}.{dt.month:02d}.{dt.year:04d}", 1)
            else:
                lcd.lcd_display_string(f"{dt.hour:02d}:{dt.minute:02d}/{dt.day:02d}.{dt.month:02d}.{dt.year:04d}", 1)

        if (not lineBlocked[1]):
            lcd.lcd_display_string(str(weather.getCurrentTemperature()) + "ßC", 2)

    match backlight:
        case 0:
            lcd.lcd_backlight("off")
        case 1:
            lcd.lcd_backlight("on")
        case 2:
            autoBacklight()

    sleep(1)
