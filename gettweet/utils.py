import os
import requests

from datetime import datetime
from dateutil.parser import parse

from requests_oauthlib import OAuth1

# grab twitter keys from env
env = os.environ
TWITTER_API_KEY = env.get('TWITTER_API_KEY')
TWITTER_API_SECRET_KEY = env.get('TWITTER_API_SECRET_KEY')
TWITTER_ACCESS_TOKEN = env.get('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = env.get('TWITTER_ACCESS_TOKEN_SECRET')

if not (TWITTER_API_KEY and TWITTER_API_SECRET_KEY and TWITTER_ACCESS_TOKEN and
        TWITTER_ACCESS_TOKEN_SECRET):
    raise KeyError('TWITTER_API_KEY, TWITTER_API_SECRET_KEY, '
                   'TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET must '
                   'be set.')

# setup authentication for requests
auth = OAuth1(
    TWITTER_API_KEY,
    TWITTER_API_SECRET_KEY,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET)


def format_data(tweets):
    """This function will format the response from Twitter API into a small and
    compact format.

    Args:
        tweets: List of tweets

    Returns:
        List of dictionaries (tweets)
    """

    return [{
        'text': tweet.get('text', ''),
        'likes': tweet.get('favorite_count', 0),
        'replies': tweet.get('reply_count', 0),
        'retweets': tweet.get('retweet_count', 0),
        'hashtags': ['#{}'.format(hashtag.get('text', ''))
            for hashtag in tweet.get('entities', {}).get('hashtags', {})],
        'date': parse(tweet.get('created_at')).strftime(
            '%-I:%-M %p - %-d %b %Y'),
        'account': {
            'fullname': tweet.get('user', {}).get('name', ''),
            'href': '/{}'.format(tweet.get('user', {}).get('screen_name', '')),
            'id': tweet.get('user', {}).get('id', ''),
        },
    } for tweet in tweets]


def send_request(url, params):
    """This function sends a request to Twitter API

    Args:
        url: String endpoint to be requested
        params: Dict containing the search parameters.

    Returns:
        JSON response from Twitter API
    """

    response = requests.get(url, params=params, auth=auth)
    return response.json(), response.status_code

def get_tweets_by_hashtag(hashtag, max_tweets=30):
    """This function will fetch the tweets with the hashtag

    Args:
        hashtag: String to be searched.
        limit: Int that determines the number of tweets to be returned.
        Default 30

    Returns:
        A list of tweets with the searched hashtag in JSON format.

    """
    url = 'https://api.twitter.com/1.1/search/tweets.json'
    params = {
        'q': '%23{}'.format(hashtag),
        'count': max_tweets,
        'include_entities': True
    }

    response, code = send_request(url, params)
    return (format_data(response.get('statuses', {}))
            if not code != 200 else response, code)

def get_tweets_by_user(username, max_tweets=30):
    """This function will fetch the tweets from a user

    Args:
        username: String username of the user.
        limit: Int that determines the number of tweets to be returned.
        Default 30

    Returns:
        A list of tweets with the searched hashtag in JSON format.

    """
    url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    params = {
        'screen_name': username,
        'count': max_tweets,
        'exclude_replies': False,
        'include_rts': True
    }

    response, code = send_request(url, params)
    return (format_data(response)
            if not code != 200 else response, code)
