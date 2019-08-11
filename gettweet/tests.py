import unittest
import json
from importlib import reload
from unittest.mock import patch

from .app import app
from gettweet import utils

class RoutesTestCase(unittest.TestCase):
    """Test Cases for app routes. """

    def setUp(self):
        """Setup test client."""
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()

    def tearDown(self):
        pass

    def generate_test_response(self, items, code=200):
        """Generate a list of dict containing expected return values.

        Args:
            hashtag: Int number of dictionaries to be generated.

        Returns:
            A list of dictionaries that represent the tweet data.
        """
        return [{
            'text': 'test-{}'.format(x),
            'likes': x,
            'replies': x,
            'retweets': x,
            'hashtags': ['#hashtag{}'.format(x)],
            'date': x,
            'account': {
                'fullname': 'name-{}'.format(x),
                'href': '/{}'.format(x),
                'id': x,
            },
        } for x in range(items)], code

    def test_get_hashtags(self):
        """Test get hashtag route. """
        with patch('gettweet.app.get_tweets_by_hashtag') as \
                get_tweets_by_hashtag:
            get_tweets_by_hashtag.return_value = \
                self.generate_test_response(30)
            response = self.app.get('/hashtags/fifa')
            self.assertEqual(response.status_code, 200)
            result = response.get_json()
            self.assertEqual(len(result), 30)

    def test_get_hashtags_with_limit(self):
        """Test get hashtag route with specified limit. """
        with patch('gettweet.app.get_tweets_by_hashtag') as \
                get_tweets_by_hashtag:
            for items in range(10):
                get_tweets_by_hashtag.return_value = \
                    self.generate_test_response(items)
                response = self.app.get(
                    '/hashtags/fifa?limit={}'.format(items))
                self.assertEqual(response.status_code, 200)
                result = response.get_json()
                self.assertEqual(len(result), items)

    def test_get_hashtags_without_args(self):
        """Test get hashtag with no specified kwargs."""
        response = self.app.get('/hashtags/')
        self.assertEqual(response.status_code, 404)

    def test_get_hashtags_invalid_args(self):
        """Test get hashtag with invalid kwargs."""
        with patch('gettweet.utils.send_request') as \
                send_request:
            send_request.return_value = {'errors': {}}, 403
            response = self.app.get('/hashtags/@')
            self.assertEqual(response.status_code, 403)

    def test_get_user_tweets(self):
        """Test get user tweet route. """
        with patch('gettweet.app.get_tweets_by_user') as \
                get_tweets_by_hashtag:
            get_tweets_by_hashtag.return_value = \
                self.generate_test_response(30)
            response = self.app.get('/users/realdonaldtrump')
            self.assertEqual(response.status_code, 200)
            result = response.get_json()
            self.assertEqual(len(result), 30)

    def test_get_user_tweets_with_limit(self):
        """Test get user tweet route with specified limit. """
        with patch('gettweet.app.get_tweets_by_user') as \
                get_tweets_by_hashtag:
            for items in range(10):
                get_tweets_by_hashtag.return_value = \
                    self.generate_test_response(items)
                response = self.app.get(
                    '/users/realdonaldtrump?limit={}'.format(items))
                self.assertEqual(response.status_code, 200)
                result = response.get_json()
                self.assertEqual(len(result), items)

    def test_get_user_tweets_without_args(self):
        """Test get user tweet route with no specified kwargs."""
        response = self.app.get('/users/')
        self.assertEqual(response.status_code, 404)

    def test_get_user_tweets_non_existent_user(self):
        """Test get user tweet route with non existent user."""
        with patch('gettweet.utils.send_request') as \
                send_request:
            send_request.return_value = {'errors': {}}, 404
            response = self.app.get('/users/xsolnine')
            self.assertEqual(response.status_code, 404)
            self.assertIn('errors', response.json)


class UtilsTestCase(unittest.TestCase):
    """Test Cases for twitter utils. """

    def validate_response(self, items):
        """Validate reponse by checking if the dictionary has complete keys

        Args:
            items: List of formatted tweets
        """
        keys = ['text', 'likes' , 'replies', 'retweets', 'hashtags', 'date',
                'account']
        account_keys = ['fullname', 'id', 'href']
        for item in items:
            self.assertTrue(all(key in item for key in keys))
            self.assertTrue(
                all(key in item['account'] for key in account_keys))

    def test_get_tweets_by_hashtag(self):
        """Test get tweets by hashtag util. """
        response, code = utils.get_tweets_by_hashtag('fifa')
        self.assertEqual(len(response), 30)
        self.assertEqual(code, 200)
        self.validate_response(response)

    def test_get_tweets_by_hashtag_with_limit(self):
        """Test get tweets by hashtag util with limit. """
        response, code = utils.get_tweets_by_hashtag('python', 5)
        self.assertEqual(len(response), 5)
        self.assertEqual(code, 200)
        self.validate_response(response)
    
    def test_get_tweets_by_hashtag_invalid(self):
        """Test get tweets by hashtag util with invalid search key. """
        response, code = utils.get_tweets_by_hashtag('@')
        self.assertEqual(code, 403)
        self.assertIn('errors', response.keys())

    def test_get_tweets_by_user(self):
        """Test get tweets by user util. """
        response, code = utils.get_tweets_by_user('realdonaldtrump')
        self.assertEqual(len(response), 30)
        self.assertEqual(code, 200)
        self.validate_response(response)

    def test_get_tweets_by_user_with_limit(self):
        """Test get tweets by user util with limit. """
        response, code = utils.get_tweets_by_user('realdonaldtrump', 10)
        self.assertEqual(len(response), 10)
        self.assertEqual(code, 200)
        self.validate_response(response)

    def test_get_tweets_by_user_not_found(self):
        """Test get tweets by user util. """
        response, code = utils.get_tweets_by_user('xsolnine', 10)
        self.assertEqual(len(response), 1)
        self.assertEqual(code, 404)
        self.assertIn('errors', response.keys())

    def test_send_request(self):
        """Test send request util. """
        expected_json = {'statuses': []}
        with patch('gettweet.utils.requests.get') as \
                requests_get:
            requests_get.return_value.json.return_value = expected_json
            requests_get.return_value.status_code = 200
            response = utils.send_request('some_url', {})
            self.assertEqual(response[0], expected_json)
            self.assertEqual(response[1], 200)

    def test_format_data(self):
        """Test format data util. """
        tweets = [{
            'text': 'text',
            'favorite_count': 10,
            'reply_count': 10,
            'retweet_count': 10,
            'entities': {
                'hashtags': [{
                    'text': 'hash'
                }]
            },
            'created_at': 'Wed Oct 10 20:19:24 +0000 2018',
            'user': {
                'name': 'name',
                'screen_name': 'name',
                'id': 1
            }
        }]

        response = utils.format_data(tweets)
        self.validate_response(response)

if __name__ == '__main__':
    unittest.main()
