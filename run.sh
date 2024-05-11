#!/bin/bash

if [ -z "$BASH_VERSION" ]
then
    echo "Please run this script with bash, not sh or any other shell."
    echo "Other shells like sh might not support virtual environments."
    exit 1
fi

echo "Activating virtual environment"
source venv/bin/activate

echo "Starting program"
sudo python3 main.py # needs root privileges because of Flask.

echo "Deactivating virtual environment"
deactivate