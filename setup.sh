#!/bin/bash

if [ -z "$BASH_VERSION" ]
then
    echo "Please run this script with bash, not sh or any other shell."
    echo "Other shells like sh might not support virtual environments."
    exit 1
fi

sudo apt update
sudo apt install -y python3 python3-pip python3-venv

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