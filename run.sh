#!/bin/bash

echo "Activating virtual environment"
source venv/bin/activate

echo "Starting program"
sudo python3 main.py # needs root privileges because of Flask.

echo "Deactivating virtual environment"
deactivate