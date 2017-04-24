#!/usr/bin/env bash
sudo apt-get install chromium-browser chromium-chromedriver python-virtualenv xvfb
mkvirtualenv crawler
pip install -r requirements.txt
