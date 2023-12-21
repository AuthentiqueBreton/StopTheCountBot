#!/usr/bin/env python3

'''
Data structure for tweet contents
'''

import logging

LOGGER = logging.getLogger(__name__)

class Tweet:
    '''
    Data structure for Tweets
    '''
    def __init__(self, text_data:str) -> None:
        text_data_list = text_data.split('\n')
        self.display_name = text_data_list[0]
        self.user_id = text_data_list[1]
        self.raw_content = []
        for tweet_element in text_data_list[4:-1]:
            try:
                int(tweet_element)
                continue
            except ValueError:
                self.raw_content.append(tweet_element)

    def check_content_limit(self, limit:int) -> bool:
        '''
        Check if the tweet content isn't too long.

        Args:
            limit (int): Maximum number of rows in the tweet.

        Returns:
            bool: Returns True if the content isn't too long else returns false.
        '''
        if len(self.raw_content) > limit:
            return False
        return True

    def check_content_repetitions(self) -> bool:
        '''
        Check if the tweet doen't contains repetitions.

        Returns:
            bool: Returns True if there is no repetitions else returns false.
        '''
        for element in self.raw_content:
            if self.raw_content.count(element) > 1:
                return False
        return True
