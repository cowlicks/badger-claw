#!/usr/bin/env bash
sudo apt-get install -y chromium-browser chromium-chromedriver python-virtualenv xvfb
virtualenv env
source env/bin/activate
pip install -r requirements.txt
