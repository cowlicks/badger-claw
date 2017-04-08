#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from glob import glob
import json
import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import top500


BASE = "chrome-extension://mcgekeccgjgcmhnhbabplanchdogjcnh/"
BACKGROUND = BASE + "_generated_background_page.html"
def get_extension_path():
    path = os.environ.get('EXTENSION_PATH', glob('*.crx'))
    if isinstance(path, list):
        if not path:
            raise ValueError("No extension found. Put a .crx file in this directory'")
        return path.pop()
    return path


# start chrome with privacy badger

# start opening websites
opts = Options()
opts.binary_location = '/usr/bin/google-chrome-stable'
opts.add_experimental_option("excludeSwitches",
                             ["ignore-certificate-errors"])
opts.add_extension(get_extension_path())
prefs = {"profile.block_third_party_cookies": False}
opts.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=opts)
for url in top500.urls[:2]:
    driver.get(url)
    sleep(1)

driver.get(BACKGROUND)

storages = ['action_map', 'snitch_map', 'action_map', 'cookieblock_list',
            'dnt_hashes', 'settings_map', 'snitch_map', 'supercookie_domains']

data = {}
for storage in storages:
    script = 'return badger.storage.%s.getItemClones()' % storage
    data[storage] = driver.execute_script(script)

with open('results.json', 'w') as f:
    f.write(json.dumps(data, indent=4, sort_keys=True))
driver.quit()
