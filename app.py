# -*- coding: utf-8 -*-

import os
import time
import click
import easygui
import yaml
import random
from glob import glob
import pygame

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

CWD = '/Users/khcho/workspaces/ypd/lilac'

MSG = 'This is automatically mapping function program for YPD'
TITLE = 'LILAC by IU'

@click.command()
@click.option('--verbose', is_flag=True, help='Print detail log')
def main(verbose):

    with open('{}/config.yaml'.format(CWD)) as f:
        config = yaml.full_load(f)
        LOGIN_URL = '{}/security/login'.format(config['host'])
        RIDING_MAPPING_STAFF_URL = '{}/riding/mappingStaff'.format(config['host'])

    images = glob('{}/images/*'.format(CWD))
    while True:
        image = images[random.randrange(0, len(images))]
        nfc_id = easygui.enterbox(MSG, title=TITLE, default='', image=image)
        if nfc_id:
            options = Options()
            options.add_argument('--disable-infobars')
            options.add_argument('--no-sandbox')
            wd = webdriver.Chrome('./webdriver/osx/chromedriver', options=options)
            wd.implicitly_wait(3)

            wd.get(LOGIN_URL)
            username_input = wd.find_element(By.NAME, 'username')
            username_input.send_keys(config.get('email'))
            password_input = wd.find_element(By.NAME, 'password')
            password_input.send_keys(config.get('password'))
            wd.find_element(By.XPATH, '//*[@id="loginForm"]/div[3]/div/button').click()

            wd.get(RIDING_MAPPING_STAFF_URL)
            wd.implicitly_wait(3)

            wd.find_element(By.XPATH, '//*[@id="wrbId"]').send_keys(nfc_id)
            button_search = wd.find_element(By.ID, 'button-search')
            if button_search:
                button_search.click()
                time.sleep(1)
                mapping_key = wd.find_element(By.XPATH, '//*[@id="list"]/tbody/tr/td[5]/div/button[1]')
                print(mapping_key)
                if mapping_key:
                    mapping_key.click()
                else:
                    print('no result for search')
            else:
                print('no result')

            time.sleep(3)
        else:
            pass

        cc = easygui.ccbox(MSG, title=TITLE, image=images[random.randrange(0, len(images))])
        if cc:
            print('contiune')
            continue
        break
    print('Exit LILAC')

if __name__=='__main__':
    main()

