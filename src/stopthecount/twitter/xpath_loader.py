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
    tweet_xpath = xpath_manager.tweet_xpath
    username_xpath = xpath_manager.username_xpath
    content_xpath = xpath_manager.content_xpath
    xpath_manager.tweet_xpath = '//div[@class="tweet_div-id"]'
    xpath_manager.username_xpath = '//div[@class="username_div-id"]'
    xpath_manager.content_xpath = '//div[@class="content_div-id"]'
'''

import logging
import json
from pathlib import Path

LOGGER = logging.getLogger(__name__)

class TwitterXPATH:
    '''
    Class for Twitter div names (xpath) load and update.
    '''
    def __init__(self) -> None:
        self.xpath_file = Path(__file__).resolve().parent / 'xpath.json'
        self.xpath_dict = self._read_json()

    def _read_json(self) -> dict:
        '''
        Read the xpath.json file and return its content.

        Returns:
            dict: xpath.json content.
        '''
        with self.xpath_file.open(mode='r', encoding='UTF-8') as json_file:
            return json.load(json_file)

    def _write_json(self, new_xpath_content:dict) -> None:
        '''
        Modify the xpath.json file.

        Args:
            new_xpath_content (dict): new xpath ids.
        '''
        with self.xpath_file.open(mode='w', encoding='UTF-8') as json_file:
            json.dump(new_xpath_content, json_file)

    @property
    def tweet_xpath(self) -> str:
        '''
        The xpath identifier for tweets.

        Returns:
            str: xpath identifier.
        '''
        return self._read_json()['tweet_xpath']

    @property
    def username_xpath(self) -> str:
        '''
        The xpath identifier for usernames.

        Returns:
            str: xpath identifier.
        '''
        return self._read_json()['username_xpath']

    @property
    def content_xpath(self) -> str:
        '''
        The xpath identifier for contents.

        Returns:
            str: xpath identifier.
        '''
        return self._read_json()['content_xpath']

    @tweet_xpath.setter
    def tweet_xpath(self, new_xpath:str) -> None:
        '''
        Modify the tweet_xpath.

        Args:
            new_xpath (str): new tweet xpath.
        '''
        self.xpath_dict['tweet_xpath'] = new_xpath
        self._write_json(self.xpath_dict)

    @username_xpath.setter
    def username_xpath(self, new_xpath:str) -> None:
        '''
        Modify the username_xpath.

        Args:
            new_xpath (str): new username xpath.
        '''
        self.xpath_dict['username_xpath'] = new_xpath
        self._write_json(self.xpath_dict)

    @content_xpath.setter
    def content_xpath(self, new_xpath:str) -> None:
        '''
        Modify the content_xpath.

        Args:
            new_xpath (str): new content xpath.
        '''
        self.xpath_dict['content_xpath'] = new_xpath
        self._write_json(self.xpath_dict)
