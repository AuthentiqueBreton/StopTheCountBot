from stopthecount.twitter.download import get_tweets
import logging
from stopthecount.processing.extract_proposals import extract_proposals

logging.basicConfig(
    style='{',
    format='[{asctime}] {levelname} {message}',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.ERROR
)

result = get_tweets('https://x.com/Pop_Kulture1/status/1791844446625018070')

extracted = extract_proposals('réalisateurs', result)

for username, response in extracted.items():
    print(f"{username}: {response}")
