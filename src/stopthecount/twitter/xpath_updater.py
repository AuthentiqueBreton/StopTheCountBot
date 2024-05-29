#!/usr/bin/env python3

'''
Module for regenerating xpaths based on HTML ID changes for tweet replies.
'''

import logging

from lxml import etree

from stopthecount.twitter.download import download_html_code
from stopthecount.twitter.xpath_loader import TwitterXPATH

LOGGER = logging.getLogger(__name__)
TWEET_URL = 'https://x.com/StopTheCountBot/status/1731861672199909757'

def regenerate_xpath(tweet_div_id:str) -> None:
    '''
    Regenerate xpaths in case of HTML ID changes.

    Args:
        tweet_div_id (str): div ID of a tweet reply.
    '''
    xpath = TwitterXPATH()
    xpath.tweet_xpath = f"//div[@class='{tweet_div_id}']"

    tweet_code_list = download_html_code(url=TWEET_URL)
    tweet_code = tweet_code_list[_find_model_idx(tweet_code_list)]

    xpath.username_xpath = _xpath_explorer(tweet_code, '@StopTheCountBot')
    xpath.content_xpath = _xpath_explorer(tweet_code, 'Typical answer model')


def _xpath_explorer(tweet_code:str, target:str) -> str:
    '''
    Allow to retrieve the path of a specific tweet element.

    Args:
        tweet_code (str): HTML code of a tweet.
        target (str): The text to retrieve.

    Returns:
        str: The xpath of the target on the tweet code.
    '''
    html_parser = etree.HTMLParser()
    html_tree = etree.ElementTree(etree.fromstring(tweet_code, html_parser))

    target_element = html_tree.xpath(f'//*[text()="{target}"]')[0]

    current_element = target_element
    path_parts = []
    while current_element is not None:
        element_id = current_element.get("id")
        element_class = current_element.get("class")

        if element_class:
            path_part = f"{current_element.tag}[@class='{element_class}']"
        elif element_id:
            path_part = f"{current_element.tag}[@id='{element_id}']"
        else:
            path_part = current_element.tag

        path_parts.append(path_part)
        current_element = current_element.getparent()

    path_parts.reverse()
    final_path = '/'.join(path_parts).replace('html/body', '/')

    return final_path

def _find_model_idx(tweet_code_list:list) -> int:
    '''
    Allow to retrieve the tweet model HTML code.

    Args:
        tweet_code_list (list): All tweet HTML codes.

    Returns:
        int: Index of the tweet model code.
    '''
    for idx, tweet_code in enumerate(tweet_code_list):
        if tweet_code.find('Typical') != -1:
            return idx
    return -1
