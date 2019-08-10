
from flask import Flask, request, jsonify

from .utils import get_tweets_by_hashtag, get_tweets_by_user


app = Flask(__name__)


@app.route('/hashtags/<string:hashtag>', methods=['GET'])
def get_tweets_by_hashtag_route(hashtag):
    """Route for getting tweets by hashtag.

    Route Args:
        hashtag: String to be searched.

    Query Args
        limit: Int that determines the number of tweets to be returned.
        Default 30

    Returns:
        A list of tweets with the searched hashtag in JSON format.

    """
    response = get_tweets_by_hashtag(hashtag, request.args.get('limit', 30))
    return jsonify(response)

@app.route('/users/<string:username>', methods=['GET'])
def get_tweets_by_user_route(username):
    """Route for getting tweets by a user.

    Route Args:
        username: String username of the user.

    Query Args
        limit: Int that determines the number of tweets to be returned.
        Default 30

    Returns:
        A list of tweets by a user in JSON format.
    """
    response = get_tweets_by_user(username, request.args.get('limit', 30))
    return jsonify(response)
