#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from glob import glob
import json
import os
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import top500


base_url = "chrome-extension://mcgekeccgjgcmhnhbabplanchdogjcnh/"
background_url = base_url + "_generated_background_page.html"
storages = ['action_map', 'snitch_map', 'action_map', 'cookieblock_list',
            'dnt_hashes', 'settings_map', 'snitch_map', 'supercookie_domains']


def get_extension_path():
    path = os.environ.get('EXTENSION_PATH', glob('*.crx'))
    if isinstance(path, list):
        if not path:
            raise ValueError("No extension found. Put a .crx file in "
                             "this directory")
        return path.pop()
    return path


def start_driver():
    opts = Options()
    opts.binary_location = '/usr/bin/google-chrome-stable'
    opts.add_extension(get_extension_path())
    opts.add_experimental_option("prefs", {"profile.block_third_party_cookies": False})
    return webdriver.Chrome(chrome_options=opts)


def save(driver):
    driver.get(background_url)
    data = {}
    for storage in storages:
        script = 'return badger.storage.%s.getItemClones()' % storage
        data[storage] = driver.execute_script(script)

    with open('results.json', 'w') as f:
        f.write(json.dumps(data, indent=4, sort_keys=True))


if __name__ == '__main__':
    driver = start_driver()
    driver.set_page_load_timeout(5)

    for url in top500.urls:
        try:
            driver.get(url)
            sleep(5)
        except TimeoutException:
            continue

    save(driver)
    driver.quit()
