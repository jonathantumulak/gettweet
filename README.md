# GetTweet Endpoints

API endpoints for fetching tweets from Twitter API

### 1. Get Tweets by Hashtag   
Get the list of tweets with the given hashtag.
```
GET http://localhost:5000/hashtags/<hashtag>?limit=30
```
Replace `hashtag` with the string you want to search.
Optional `limit` to specify how many tweets you want to fetch.

Sample
```
$ curl -H "Accept: application/json" -X GET http://localhost:5000/hashtags/donaldtrump?limit=30
```
```
Response:
[
  {
    "account": {
      "fullname": "Forrester", 
      "href": "/InYourMindead", 
      "id": 986272227426320384
    }, 
    "date": "10:54 AM - 10 Aug 2019", 
    "hashtags": [
      "#DonaldTrump"
    ], 
    "likes": 0, 
    "replies": 0, 
    "retweets": 276, 
    "text": "RT @glamelegance: He\u2019s a hero but the so-called President #DonaldTrump couldn\u2019t remember his name seconds after meeting him?? \nIt\u2019s Army Pr\u2026"
  }, 
  ...
]
```

### 2. Get Tweets by User
Get the list of tweets that the user has on their feed.
```
GET http://localhost:5000/users/<username>?limit=30
```
Replace `username` with the username you want to search.
Optional `limit` to specify how many tweets you want to fetch.

Sample
```
$ curl -H "Accept: application/json" -X GET http://localhost:5000/users/realdonaldtrump?limit=30
```

```
Response:
[
   {
    "account": {
      "fullname": "Donald J. Trump", 
      "href": "/realDonaldTrump", 
      "id": 25073877
    }, 
    "date": "6:44 PM - 9 Aug 2019", 
    "hashtags": [], 
    "likes": 111727, 
    "replies": 0, 
    "retweets": 25317, 
    "text": "....to inflame and cause chaos. They create their own violence, and then try to blame others. They are the true Rac\u2026 https://t.co/r6f1K8zGkk"
  }, 
  ...
]
```

## Installation

To run the project:

1. Install [Docker](https://www.docker.com/products/docker-desktop)
2. Pull Repository and `cd` into the repo
```
git clone git@github.com:jonathantumulak/gettweet.git
cd gettweet
```
3. Create a `.env` file from the contents of `env.example`. Replace the following keys with your own API Keys. Create a twitter app from [here](https://developer.twitter.com/en/apps). You can use the one provided in `env.example` if you dont have one.
```
TWITTER_API_KEY=...
TWITTER_API_SECRET_KEY=...
TWITTER_ACCESS_TOKEN=...
TWITTER_ACCESS_TOKEN_SECRET=...
```
4. Start development server with the command:
```
$ docker-compose up --build
```

5. Open a Browser/REST Client and access the urls specified above.

To run the project in the background:
```
$ docker-compose up -d
```

To stop the project running in the background:
```
$ docker-compose stop
```

## Tests

To run tests:
```
$ docker-compose -f docker-compose.test.yml up --build
```
