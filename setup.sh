#!/bin/bash
# Install dependencies.
sudo apt update
sudo apt install git python3 idle3 pip3

# Clone repo.
cd /home/pi
git clone https://github.com/rustygreen/raspberry-pi-server.git
cd raspberry-pi-server

# Run server.
pip3 install -r requirements.txt
sudo python3 server.py

echo "Server is running on http://localhost:8080"