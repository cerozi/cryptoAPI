from requests import Response
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Crypto

# /* tests for the 'overal/' url */

class OverallTest(APITestCase):
    
    # get method
    def test_get_cryptos(self):
        response = self.client.get(reverse('overall'))
        self.assertEqual(200, response.status_code)
    
    # post method
    def test_post_crypto(self):
        data = {
            'name': 'bitcoin'
        }

        response = self.client.post(reverse('overall'), data)
        self.assertEqual(201, response.status_code)
    
    # post method with invalid crypto name
    def test_post_wrong_crypto(self):
        data = {
            'name': 'asdasd'
        }

        response = self.client.post(reverse('overall'), data)
        self.assertEqual(400, response.status_code)

class OverallTestII(APITestCase):

    # creates 5 crypto's
    def setUp(self):
        list = ['bitcoin', 'ethereum', 'tether', 'bnb', 'cosmos']
        for crypto in list:
            Crypto.objects.create(name=crypto)

    # try to add more crypto to the dashboard
    def test_post(self):
        data = {
            'name': 'cronos'
        }

        response = self.client.post(reverse('overall'), data)
        self.assertEqual(405, response.status_code)

# /* tests for the 'overal/<slug:slug>' url */

class OverallSlugTest(APITestCase):

    # creates crypto
    def setUp(self):
        self.bitcoin = Crypto(name='bitcoin')
        self.bitcoin.save()

    # get crypto detail
    def test_get(self):
        response = self.client.get(reverse('crypto-detail', args=(self.bitcoin.slug, )))
        self.assertEqual(200, response.status_code)

    # try to get unexisting crypto detail
    def test_get_wrong_crypto(self):
        response = self.client.get(reverse('crypto-detail', args=('ethereum', )))
        self.assertEqual(400, response.status_code)

    # delete method
    def test_delete(self):
        response = self.client.delete(reverse('crypto-detail', args=(self.bitcoin.slug, )))
        self.assertEqual(204, response.status_code)

    # >>>> paramether testing <<<<<


# /* tests for the 'convert' url */

class ConvertTest(APITestCase):

    # creates cryptos
    def setUp(self):
        self.bitcoin = Crypto.objects.create(name='bitcoin')
        self.ethereum = Crypto.objects.create(name='ethereum')

    # tests conversion
    def test_post_convert(self):
        data = {
            'fromCoin': self.bitcoin.name,
            'toCoin': self.ethereum.name,
            'amount': 1
        }

        response = self.client.post(reverse('convert'), data)
        self.assertEqual(200, response.status_code)

        # tests conversion with unexisting cryptos
        wrongData = {
            'fromCoin': 'asdasda',
            'toCoin': 'asdasdsa',
            'amount': 1
        }

        response = self.client.post(reverse('convert'), wrongData)
        self.assertEqual(404, response.status_code)