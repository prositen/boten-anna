from functools import lru_cache

import requests
from bs4 import BeautifulSoup

from plugins.restaurants.common import add_restaurant, Lunch, Item


@add_restaurant
class Marrakech(Lunch):
    url = 'https://www.cafemarrakech.se/meny'

    @staticmethod
    def name():
        return 'Marrakech'

    @staticmethod
    def minutes():
        return 5

    @lru_cache(32)
    def get(self, year, month, day):
        return [
            Item(name="Buffé")
        ]
