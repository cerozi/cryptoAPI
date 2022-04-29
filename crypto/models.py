from django.db import models
from django.utils.text import slugify
import requests


url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?CMC_PRO_API_KEY=b8e818b8-bd7c-44a1-a762-7fff9b1b1b35&slug={}'

# Create your models here.
class Crypto(models.Model):
    name = models.CharField(max_length=50, unique=True)
    symbol = models.CharField(max_length=5, unique=True, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    price = models.FloatField(blank=True, null=True)
    last_24h = models.FloatField(blank=True, null=True)
    last_7d = models.FloatField(blank=True, null=True)
    date = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        self.name = self.name.lower()

        response = requests.get(url.format(self.name)).json()
        coin_id = list(response['data'].keys())[0]
        self.symbol = response['data'][f'{coin_id}']['symbol']
        self.price = round(response['data'][f'{coin_id}']['quote']['USD']['price'], 2)
        self.last_24h = round(response['data'][f'{coin_id}']['quote']['USD']["percent_change_24h"], 2)
        self.last_7d = round(response['data'][f'{coin_id}']['quote']['USD']["percent_change_7d"], 2)
        self.slug = slugify(self.name)

        return super().save(*args, **kwargs)
