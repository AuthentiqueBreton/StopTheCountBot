#!/usr/bin/env python3

'''
Module for managing and updating XPaths (div names) related to Twitter elements.
'''

import logging
import json

from xdg_base_dirs import xdg_cache_home

LOGGER = logging.getLogger(__name__)

class TwitterXPATH:
    '''
    Class for Twitter div names (xpath) load and update.
    '''
    def __init__(self) -> None:
        self.xpath_file = xdg_cache_home() / 'STC' / 'xpath.json'
        self.xpath_file.parent.mkdir(parents=True, exist_ok=True)

        self.xpath_dict = {
            'tweet_xpath': None,
            'username_xpath': None,
            'content_xpath': None
        }

        if self.xpath_file.exists():
            try:
                self.xpath_dict.update(self._read_json())
            except json.JSONDecodeError:
                LOGGER.error('Failed decoding JSON from %s, using default values.', self.xpath_file)

        self._write_json(self.xpath_dict)

    def _read_json(self) -> dict:
        '''
        Read the xpath.json file and return its content.

        Returns:
            dict: xpath.json content.
        '''
        try:
            with self.xpath_file.open(mode='r', encoding='UTF-8') as json_file:
                return json.load(json_file)
        except FileNotFoundError:
            LOGGER.error('File %s not found.', self.xpath_file)
            return {}
        except json.JSONDecodeError:
            LOGGER.error('Error decoding JSON from %s.', self.xpath_file)
            return {}

    def _write_json(self, new_xpath_content: dict) -> None:
        '''
        Modify the xpath.json file.

        Args:
            new_xpath_content (dict): new xpath ids.
        '''
        try:
            with self.xpath_file.open(mode='w', encoding='UTF-8') as json_file:
                json.dump(new_xpath_content, json_file, indent=4)
        except IOError as e:
            LOGGER.error('Error writing to %s : %s', self.xpath_file, e)

    def _update_xpath(self, key: str, new_xpath: str) -> None:
        '''
        Update the xpath value for a given key and write to the JSON file.

        Args:
            key (str): The key to update.
            new_xpath (str): The new xpath value.
        '''
        self.xpath_dict[key] = new_xpath
        self._write_json(self.xpath_dict)

    @property
    def tweet_xpath(self) -> str:
        '''
        The xpath identifier for tweets.

        Returns:
            str: xpath identifier.
        '''
        return self.xpath_dict['tweet_xpath']

    @property
    def username_xpath(self) -> str:
        '''
        The xpath identifier for usernames.

        Returns:
            str: xpath identifier.
        '''
        return self.xpath_dict['username_xpath']

    @property
    def content_xpath(self) -> str:
        '''
        The xpath identifier for contents.

        Returns:
            str: xpath identifier.
        '''
        return self.xpath_dict['content_xpath']

    @tweet_xpath.setter
    def tweet_xpath(self, new_xpath: str) -> None:
        '''
        Modify the tweet_xpath.

        Args:
            new_xpath (str): new tweet xpath.
        '''
        self._update_xpath('tweet_xpath', new_xpath)

    @username_xpath.setter
    def username_xpath(self, new_xpath: str) -> None:
        '''
        Modify the username_xpath.

        Args:
            new_xpath (str): new username xpath.
        '''
        self._update_xpath('username_xpath', new_xpath)

    @content_xpath.setter
    def content_xpath(self, new_xpath: str) -> None:
        '''
        Modify the content_xpath.

        Args:
            new_xpath (str): new content xpath.
        '''
        self._update_xpath('content_xpath', new_xpath)
