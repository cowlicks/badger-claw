#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from glob import glob
import json
import os
from time import sleep
from contextlib import contextmanager

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

import top500


base_url = "chrome-extension://mcgekeccgjgcmhnhbabplanchdogjcnh/"
background_url = base_url + "_generated_background_page.html"
storages = ['action_map', 'snitch_map', 'action_map', 'cookieblock_list',
            'dnt_hashes', 'settings_map', 'snitch_map', 'supercookie_domains']

@contextmanager
def xvfb_manager():
    wants_xvfb = bool(int(os.environ.get("ENABLE_XVFB", 0)))
    if wants_xvfb:
        from xvfbwrapper import Xvfb

        vdisplay = Xvfb(width=1280, height=720)
        vdisplay.start()
        try:
            yield vdisplay
        finally:
            vdisplay.stop()
    else:
        yield

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
    opts.add_argument('--dns-prefetch-disable')
    return webdriver.Chrome(chrome_options=opts)


def save(driver):
    driver.get(background_url)
    data = {}
    for storage in storages:
        script = 'return badger.storage.%s.getItemClones()' % storage
        data[storage] = driver.execute_script(script)

    with open('results.json', 'w') as f:
        f.write(json.dumps(data, indent=4, sort_keys=True))
    print('Data saved successfully.')


def timeout_workaround(driver):
    '''
    Selenium has a bug where a tab that raises a timeout exception can't recover
    gracefully. So we kill the tab and make a new one.
    '''
    driver.close()  # kill the broken site
    driver.switch_to_window(driver.window_handles.pop())
    before = set(driver.window_handles)
    driver.execute_script('window.open()')
    driver.switch_to_window((set(driver.window_handles) ^ before).pop())
    return driver


if __name__ == '__main__':
    timeout = 10
    driver = start_driver()
    driver.set_page_load_timeout(timeout)
    driver.set_script_timeout(timeout)

    for url in top500.urls:
        try:
            print('visiting %s' % url)
            driver.get(url)
            sleep(timeout)
        except TimeoutException as e:
            print('timeout on %s ' % url)
            driver = timeout_workaround(driver)
            continue

    save(driver)
    driver.quit()
