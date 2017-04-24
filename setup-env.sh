#!/usr/bin/env bash
sudo apt-get install -y chromium-browser chromium-chromedriver python-virtualenv xvfb virtualenvwrapper
mkvirtualenv crawler
pip install -r requirements.txt
