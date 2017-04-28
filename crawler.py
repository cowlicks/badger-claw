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
from logger import logger


base_url = "chrome-extension://mcgekeccgjgcmhnhbabplanchdogjcnh/"
background_url = base_url + "_generated_background_page.html"
storages = ['action_map', 'snitch_map', 'action_map', 'cookieblock_list',
            'dnt_hashes', 'settings_map', 'snitch_map', 'supercookie_domains']

@contextmanager
def xvfb_manager():
    wants_xvfb = bool(int(os.environ.get("ENABLE_XVFB", 1)))
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
    logger.info('Using extension at %s' % path)
    return path


def start_driver():
    opts = Options()
    opts.add_extension(get_extension_path())
    opts.add_experimental_option("prefs", {"profile.block_third_party_cookies": False})
    opts.add_argument('--dns-prefetch-disable')
    chromedriver_path = os.environ.get(
            'CHROMEDRIVER_PATH',
            '/usr/lib/chromium-browser/chromedriver')
    return webdriver.Chrome(chromedriver_path, chrome_options=opts)


def save(driver):
    out_file = os.environ.get('OUT_FILE', 'results.json')
    driver.get(background_url)
    data = {}
    for storage in storages:
        script = 'return badger.storage.%s.getItemClones()' % storage
        data[storage] = driver.execute_script(script)

    with open(out_file, 'w') as f:
        f.write(json.dumps(data, indent=4, sort_keys=True))
    logger.info('Data saved successfully to %s' % out_file)


def timeout_workaround(driver):
    '''
    Selenium has a bug where a tab that raises a timeout exception can't
    recover gracefully. So we kill the tab and make a new one.
    '''
    driver.close()  # kill the broken site
    driver.switch_to_window(driver.window_handles.pop())
    before = set(driver.window_handles)
    driver.execute_script('window.open()')
    driver.switch_to_window((set(driver.window_handles) ^ before).pop())
    return driver


def main(timeout=7, n_urls=len(top500.urls)):
    with xvfb_manager():
        driver = start_driver()
        driver.set_page_load_timeout(timeout)
        driver.set_script_timeout(timeout)

        for url in top500.urls[:n_urls]:
            try:
                logger.info('visiting %s' % url)
                driver.get(url)
                sleep(timeout)
            except TimeoutException as e:
                logger.info('timeout on %s ' % url)
                driver = timeout_workaround(driver)
                continue

        save(driver)
        driver.quit()


if __name__ == '__main__':
    main()
