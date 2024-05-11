# Time, Date and Temperature Display

## Features
* Show time, date and temperature (from openweathermap.org api) on a lcd, using a Raspberry Pi
* Backlight control using Webserver, Button and Light Sensor
* Configuration file for enabling/disabling and setting up the display, weather api and backlight control methods

## Components
* Raspberry Pi (running Linux)
* LCD (recommended: 4 lines and 20 columns; minimum: 2 lines and 16 columns*
* Button (optional)
* Ambient Light Sensor with Digital Output (optional, something like https://www.amazon.de/dp/B07DP1YM5X)

\* the 16 columns variant includes some shorter and less readable text and isn't tested as well.

## Setup
First, connect all your components to the Raspberry Pi. If you don't know how, just look up some guides on the internet.

When your wiring is complete, let's setup the python program!

1. Clone the repository (for example into your home directory)\
   `git clone https://github.com/manolol1/pi_lcd.git && cd pi_lcd`
   
2. Run the setup script, that installs all necessary programs and creates a python venv with all dependencies. You could also do that yourself, if you want.\
   `bash setup.sh`

3. Run the program for the first time to generate a config file\
   `bash run.sh`

4. Open the config file\
   `nano config.ini`\
   and make some changes:
   * Enter the number of lines and columns for your LCD module.
   * Register for the openweathermap API (free plan): https://openweathermap.org/api and set your API Key.
   * Fill in your weather location (City)
   * Optionally enable the webserver, button and/or lightsensor and set their port or pins

5. Run the program again, and check if it works.\
   `bash run.sh`

Now, you can always start the program by executing the run.sh script.

## Config file

Here is a sample config.ini file with some explanation of the different values:

```
[general]
default_backlight = 1 # state, that the backlight is in at the start of the program - 0: off, 1: on, 2: auto (controlled by light sensor)
lcd_lines = 4 # number of lines, that the lcd module has. Usually 2 or 4.
lcd_columns = 20 # number of columns, that the lcd module has. Usually 16 or 20.

[weather]
api_key = 32abgger963h535j76kli310ee52ab67 # API key from openweathermap.org, usually 32 characters long
location = Vienna # Location, that is used to request the temperature from the API
refresh_interval = 300 # time between weather data refreshs in seconds. Don't set this too low to avoid exceeding your free API call quota.

[webserver]
enabled = true
port = 85 # network port for the webserver

[button]
enabled = true
pin = 6 # GPIO pin number for the light sensor (BCM numbering)

[lightsensor]
enabled = true
pin = 16 # GPIO pin number for the light sensor (BCM numbering)

```
