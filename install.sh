#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed. Please install Python 3.7 or later and try again."
    exit 1
fi

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install the required packages
pip install -r requirements.txt

# Install Playwright browsers
playwright install

echo "Installation complete. Activate the virtual environment with 'source venv/bin/activate' before running the script."
