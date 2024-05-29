#!/usr/bin/env python3
# pylint: disable=c-extension-no-member

"""
Module to fetch tweets from a given URL and save them locally in JSON format.
"""

import json
import logging
import re
import time

import appdirs
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from xdg_base_dirs import xdg_data_home

from stopthecount.twitter.xpath_loader import TwitterXPATH

LOGGER = logging.getLogger(__name__)
CHROME = appdirs.user_data_dir(appname='Chrome', appauthor='Google')

def get_tweets(url: str) -> dict:
    """
    Retrieve tweets from a given URL. If the tweets have been previously saved locally,
    load them from the local file. Otherwise, download them and save locally.

    Args:
        url (str): The URL of the tweet.

    Returns:
        dict: A dictionary containing the tweets.
    """
    LOGGER.info("Fetching tweets from URL: %s", url)
    pattern = r"https://x.com/(?P<username>\w+)/status/(?P<tweet_id>\d+)"
    match = re.search(pattern, url)
    if not match:
        LOGGER.error("URL does not match the expected pattern.")
        raise ValueError("URL does not match the expected pattern.")

    username = match.group("username")
    tweet_id = match.group("tweet_id")
    LOGGER.info("Extracted username: %s and tweet_id: %s", username, tweet_id)

    file_dir = xdg_data_home() / 'STC' / username / tweet_id / 'raw.json'
    file_dir.parent.mkdir(parents=True, exist_ok=True)
    LOGGER.info("Local storage path: %s", file_dir)

    try:
        with file_dir.open(mode='r', encoding='UTF-8') as json_file:
            tweet_dict = json.load(json_file)
            LOGGER.info("Loaded tweets from local file.")
    except (FileNotFoundError, json.JSONDecodeError):
        LOGGER.info("Local file not found or invalid. Downloading tweets.")
        html_code_list = download_html_code(url)
        tweet_dict = extract_tweets(html_code_list)
        with file_dir.open(mode='w', encoding='UTF-8') as json_file:
            json.dump(tweet_dict, json_file, indent=4)
            LOGGER.info("Saved tweets to local file.")

    return tweet_dict

def download_html_code(url: str) -> list:
    """
    Download tweet HTML codes from a given URL using Selenium to control a web browser.

    Args:
        url (str): The URL of the tweet.

    Returns:
        list: A list of tweet HTML codes.
    """
    LOGGER.info("Starting browser to download tweets from URL: %s", url)
    options = webdriver.ChromeOptions()
    options.add_argument(f'--user-data-dir={CHROME}/User Data')
    options.add_argument('--profile-directory=Default')
    driver = webdriver.Chrome(options=options)

    xpath = TwitterXPATH()

    driver.get(url)
    wait = WebDriverWait(driver, 10)
    last_height = driver.execute_script('return document.body.scrollHeight')

    html_code_list = []
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        wait.until(ec.presence_of_all_elements_located((By.XPATH, xpath.tweet_xpath)))
        time.sleep(5)

        elements = driver.find_elements(By.XPATH, xpath.tweet_xpath)
        for element in elements:
            html_code = element.get_attribute('innerHTML')
            if html_code not in html_code_list:
                html_code_list.append(html_code)

        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == last_height:
            LOGGER.info("Reached end of page.")
            break
        last_height = new_height

    driver.quit()
    LOGGER.info("Browser closed.")

    return html_code_list

def extract_tweets(html_code_list: list) -> dict:
    """
    Extract tweet content from a list of HTML codes.

    Args:
        html_code_list (list): A list of HTML codes containing tweets.

    Returns:
        dict: A dictionary containing the tweets with usernames as keys and tweet contents as values.
    """
    xpath = TwitterXPATH()
    tweet_dict = {}
    if html_code_list:
        html_code_list.pop(0)  # Remove the first element (original tweet)
        LOGGER.info("Removed the first tweet element from the list.")

    for html_code in html_code_list:
        html_tree = etree.ElementTree(etree.fromstring(html_code, parser=etree.HTMLParser()))
        try:
            username = html_tree.xpath(xpath.username_xpath)[0].text
            content = html_tree.xpath(xpath.content_xpath)[0].text
            LOGGER.info("Extracted tweet from user: %s", username)
        except IndexError:
            LOGGER.warning("Failed to extract tweet data from HTML element.")
            continue
        tweet_dict[username] = content

    LOGGER.info("Downloaded %d tweets.", len(tweet_dict))
    return tweet_dict
