from functools import lru_cache

import requests
from bs4 import BeautifulSoup

from plugins.restaurants.common import add_restaurant, Lunch, Item


@add_restaurant
class Hogkvarteret(Lunch):
    url = 'https://hogkvarteret.wegotedge.com/scrape.php'

    @staticmethod
    def name():
        return 'Högkvarteret'

    @staticmethod
    def minutes():
        return 12

    @lru_cache(32)
    def get(self, year, month, day):
        result = requests.get(self.url)
        soup = BeautifulSoup(result.content, 'lxml')
        menu_items = []
        items_block = soup.find('span', {'class': 'itemName'}).get_text()
        for item in items_block.split('-'):
            if item:
                menu_items.append(Item(name=item.strip()))

        return menu_items

