#!/usr/bin/env python3

'''
Module for downloading tweets and handling their content from a specified URL.

Uses Selenium and Chrome to navigate the specified URL, scroll through the page to load tweets,
and provides methods to extract usernames, proposals, and handle tweet contents.

Requires:
    - appdirs: https://pypi.org/project/appdirs/
    - selenium: https://pypi.org/project/selenium/
    - Chrome browser installed

Usage:
    1. Create an instance of the Downloader class with a target URL.
    2. Utilize methods to retrieve tweet data, usernames, and proposals.

Example:
    downloader = Downloader('https://twitter.com/Username/status/some_numbers')
    downloader.get_proposals_from_username('@Username')
    downloader.get_usernames_from_proposal('Proposal')
'''

import logging
import time

import appdirs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from stopthecount.twitter.xpath_loader import TwitterXPATH

LOGGER = logging.getLogger(__name__)
CHROME = appdirs.user_data_dir(appname='Chrome', appauthor='Google')

class Downloader:
    '''
    Allow to download tweets users and contents for a given URL and handle them.
    '''
    def __init__(self, url) -> None:
        self.url = url
        self.tweets = {}
        self.content = self._download()

    def _setup_driver(self) -> webdriver.Chrome:
        '''
        Return an instance of Selenium webdriver.

        Returns:
            webdriver.Chrome: an instancied driver with specific parameters.
        '''
        options = webdriver.ChromeOptions()
        options.add_argument(f'--user-data-dir={CHROME}/User Data')
        options.add_argument('--profile-directory=Default')
        options.add_argument('--window-size=2560,1440')
        return webdriver.Chrome(options=options)

    def _download(self):
        '''
        Download the tweets at specified url and put them in a dict that map
        the username with the tweet content.
        '''
        driver = self._setup_driver()
        xpath = TwitterXPATH()

        driver.get(self.url)
        wait = WebDriverWait(driver, 10)
        last_height = driver.execute_script('return document.body.scrollHeight')

        html_code_list = []
        while True:
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            wait.until(ec.presence_of_all_elements_located((By.XPATH, xpath.tweet_xpath)))
            time.sleep(2)

            elements = driver.find_elements(By.XPATH, xpath.tweet_xpath)
            for element in elements:
                html_code = element.get_attribute('innerHTML')
                if html_code not in html_code_list:
                    html_code_list.append(html_code)

            new_height = driver.execute_script('return document.body.scrollHeight')
            if new_height == last_height:
                break
            last_height = new_height

        driver.quit()

        return html_code_list

    def get_proposals_from_username(self):
        '''
        A faire : retourne un objet qui contient les réponses brutes et des méthodes pour obtenir
        ses différentes versions.
        '''
        return None

    def get_usernames_from_proposal(self):
        '''
        A faire : parcourir les propositions et retourner les personnes qui ont envoyé une même
        proposition.
        '''
        return None
