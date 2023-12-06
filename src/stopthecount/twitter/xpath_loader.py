#!/usr/bin/env python3

'''
Module for managing and updating XPaths (div names) related to Twitter elements.

Handles loading, updating, and retrieving XPaths for usernames and tweets stored
in a JSON file ('xpath.json').

Usage:
    1. Instantiate the TwitterXPATH class to manage Twitter XPaths.
    2. Use methods to read, update, and retrieve specific XPaths.

Example:
    xpath_manager = TwitterXPATH()
    username_xpath = xpath_manager.username_xpath
    tweet_xpath = xpath_manager.tweet_xpath
    xpath_manager.set_username_xpath('//div[@class="username_div-id"]')
    xpath_manager.set_tweet_xpath('//div[@class="tweet_div-id"]')
'''

import logging
import json
from pathlib import Path
import os

LOGGER = logging.getLogger(__name__)

class TwitterXPATH:
    '''
    Class for Twitter div names (xpath) load and update.
    '''
    def __init__(self) -> None:
        self.xpath_file = Path(os.path.dirname(os.path.abspath(__file__))) / 'xpath.json'

    def _read_json(self) -> dict:
        '''
        Read the xpath.json file and return its content.

        Returns:
            dict: xpath.json content.
        '''
        with open(self.xpath_file, mode='r', encoding='UTF-8') as json_file:
            return json.load(json_file)

    def _write_json(self, new_xpath_content:dict) -> None:
        '''
        Modify the xpath.json file.

        Args:
            new_xpath_content (dict): new xpath ids.
        '''
        with open(self.xpath_file, mode='w', encoding='UTF-8') as json_file:
            json.dump(new_xpath_content, json_file)

    def set_username_xpath(self, new_xpath:str) -> None:
        '''
        Modify the username_xpath.

        Args:
            new_xpath (str): new username xpath.
        '''
        xpath_dict = self._read_json()
        xpath_dict['username_xpath'] = new_xpath
        self._write_json(xpath_dict)

    def set_tweet_xpath(self, new_xpath:str) -> None:
        '''
        Modify the tweet_xpath.

        Args:
            new_xpath (str): new tweet xpath.
        '''
        xpath_dict = self._read_json()
        xpath_dict['tweet_xpath'] = new_xpath
        self._write_json(xpath_dict)

    @property
    def username_xpath(self) -> str:
        '''
        Return the xpath identifier for usernames.

        Returns:
            str: xpath identifier.
        '''
        return self._read_json()['username_xpath']

    @property
    def tweet_xpath(self) -> str:
        '''
        Return the xpath identifier for tweets

        Returns:
            str: xpath identifier
        '''
        return self._read_json()['tweet_xpath']
