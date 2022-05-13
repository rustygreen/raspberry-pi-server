#!/bin/bash
# The following script will run the raspberry-pi-server via the manual
# setup/installation process. It is recommended to use docker instead,
# but this is a good option if you don't use containers.

# Install dependencies.
sudo apt update
sudo apt install git python3 idle3 pip3

# Clone repo.
cd /home/pi
git clone https://github.com/rustygreen/raspberry-pi-server.git
cd raspberry-pi-server

# Run server.
pip3 install -r requirements.txt
sudo python3 ./src/server.py

echo "Server is running on http://localhost:5000"