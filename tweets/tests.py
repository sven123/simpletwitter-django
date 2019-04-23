from django.test import TestCase
from tweets.models import Tweet
from rest_framework.test import APIClient


class TweetsTest(TestCase):
    fixtures = ['data']

    def setUp(self):
        self.client = APIClient()

    def test_create_tweet(self):
        response = self.client.post(
            '/tweets/',
            {'body': 'the quick brown fox', 'tag': 'lazydog'},
            format='json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            Tweet.objects.get(tag='lazydog').body,
            'the quick brown fox'
        )

    def test_get_tweets(self):
        response = self.client.get('/tweets/')
        self.assertEqual(len(response.json()), 100)

        response = self.client.get('/tweets/?start=2009-01-01&end=2012-01-01')
        self.assertEqual(len(response.json()), 23)

        response = self.client.get('/tweets/?start=2012-01-01&end=2009-01-01')
        self.assertEqual(len(response.json()), 0)

        response = self.client.get('/tweets/?tag=SpinningYearling')
        self.assertEqual(len(response.json()), 10)

        response = self.client.get(
            '/tweets/?start=2009-01-01&end=2012-01-01&tag=spinningyearling'
        )
        self.assertEqual(len(response.json()), 3)

    def test_summary(self):
        response = self.client.get('/tweets/summary/')
        self.assertEqual(len(response.json()), 15)

        response = self.client.get('/tweets/summary/?timeframe=year')
        self.assertEqual(len(response.json()), 15)

        response = self.client.get('/tweets/summary/?timeframe=month')
        self.assertEqual(len(response.json()), 74)

        response = self.client.get('/tweets/summary/?timeframe=day')
        self.assertEqual(len(response.json()), 100)

        response = self.client.get(
            '/tweets/summary/?timeframe=year&start=2008-01-01&end=2011-01-01'
        )
        self.assertEqual(len(response.json()), 3)

        response = self.client.get('/tweets/summary/?tag=bluehammerhead')
        self.assertEqual(len(response.json()), 5)
