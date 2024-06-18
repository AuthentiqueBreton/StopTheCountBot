#!/usr/bin/env python3

'''
TO DO
'''

import asyncio

from openai import AsyncOpenAI

def extract_proposals(subject:str, tweets_dict:dict) -> dict:
    '''
    _summary_

    Args:
        tweets_dict (dict): _description_

    Returns:
        dict: _description_
    '''
    return asyncio.run(send_tasks(subject, tweets_dict))


async def send_tasks(subject:str, tweets_dict:dict) -> dict:
    '''
    _summary_

    Args:
        tweet_dict (dict): _description_

    Returns:
        dict: _description_
    '''
    tasks = [ask_gpt(subject, username, content) for username, content in tweets_dict.items()]
    results = await asyncio.gather(*tasks)
    return {username: content for username, content in results if content != 'None'}


async def ask_gpt(subject:str, username:str, tweet_content:str):
    '''
    _summary_

    Args:
        subject (str): _description_
        tweet_content (str): _description_

    Returns:
        _type_: _description_
    '''
    request = (
    f"Extrait-moi la liste des {subject} présents dans le texte ci-dessous en respectant "
    "les conditions suivantes : "
    "1. Utilise les noms complets. "
    "2. Sépare chaque nom par le symbole |. "
    "3. Si aucune proposition n'est trouvée dans l'ensemble du texte, alors réponds uniquement 'None'. "
    f"Voici le texte en question : {tweet_content}"
    )

    response = await CLIENT.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": request
            }
        ],
        model="gpt-3.5-turbo-0125",
    )
    return username, response.choices[0].message.content
