#!/bin/bash

sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv

echo "Creating virtual environment"
python3 -m venv venv

echo "Activating virtual environment"
source venv/bin/activate

echo "Upgrading pip"
pip install --upgrade pip

echo "Installing dependencies"
pip install -r requirements.txt

echo "Deactivating virtual environment"
deactivate

echo "Setup complete"
echo "Run run.sh to start the program!"